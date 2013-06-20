using System;
using System.Collections.Generic;
using System.Linq;
using MathNet.Numerics.LinearAlgebra.Double;
using MathNet.Numerics.LinearAlgebra.Generic;
using Tomorrow.Mathematics;

namespace Tomorrow.Lppl
{
  public class LpplGradient
  {
    private readonly Lppl _l;

    private readonly Dictionary<double, double> _values;

    private readonly List<Dictionary<string, Func<double, double>>> _functionsDerivatives =
      new List<Dictionary<string, Func<double, double>>>();

    public LpplGradient(Lppl l, Dictionary<double, double> values)
    {
      _l = l;
      _values = values;

      _functionsDerivatives.Add(new Dictionary<string, Func<double, double>>
                                 {
                                   {"M", x => 0},
                                   {"Omega", x => 0},
                                   {"Tc", x => 0}
                                 });

      _functionsDerivatives.Add(new Dictionary<string, Func<double, double>>
                                 {
                                   {"M", x => Math.Log(_l.Tc-x) * _l.F(x)},
                                   {"Omega", x => 0},
                                   {"Tc", x => _l.M * _l.F(x) / (_l.Tc - x)}
                                 });

      _functionsDerivatives.Add(new Dictionary<string, Func<double, double>>
                                 {
                                   {"M", x => Math.Log(_l.Tc-x) * _l.G(x)},
                                   {"Omega", x => - Math.Log(_l.Tc-x) * _l.H(x)},
                                   {"Tc", x => (-_l.Omega * _l.H(x) + _l.M * _l.G(x)) / (_l.Tc - x)}
                                 });

      _functionsDerivatives.Add(new Dictionary<string, Func<double, double>>
                                 {
                                   {"M", x => Math.Log(_l.Tc-x) * _l.H(x)},
                                   {"Omega", x => Math.Log(_l.Tc-x) * _l.G(x)},
                                   {"Tc", x => (_l.Omega * _l.G(x) + _l.M * _l.H(x)) / (_l.Tc - x)}
                                 });
    }

    public DenseVector Gradient(double t)
    {
      var deltaT = _l.Tc - t;

      var gradient = new DenseVector(3);
      gradient[0] = Math.Log(deltaT) * (_l.Value(t) - _l.A);


      gradient[1] = Math.Log(deltaT) * (_l.C2 * _l.G(t) - _l.C1 * _l.H(t));

      gradient[2] = _l.M * _l.B * _l.F(t);
      gradient[2] += (_l.M * _l.C1 + _l.Omega * _l.C2) * _l.G(t);
      gradient[2] += (_l.M * _l.C2 - _l.Omega * _l.C1) * _l.H(t);
      gradient[2] /= deltaT;

      var linearGradient = LinearGradient();

      var nonLinearGradientResult = linearGradient(t);
      gradient += nonLinearGradientResult;
      //Console.WriteLine(nonLinearGradientResult);

      return gradient;
    }

    private Func<double, DenseVector> LinearGradient()
    {
      var ys = _values.Select(v => _l.Value(v.Key)).ToList();
      var fs = _l.Functions.Select(f => _values.Select(v => f(v.Key)).ToList()).ToList();
      var dfs = _functionsDerivatives
        .Select(dpf => dpf.Select(df => _values.Select(v => df.Value(v.Key)).ToList()).ToList()).ToList();

      var n = _l.Functions.Count;
      const int nb = 3;

      var results = new List<Vector<double>>();
      for (var b = 0; b < nb; b++)
      {
        var matrix = new DenseMatrix(n, n);
        var vector = new DenseVector(n);
        for (var i = 0; i < n; i++)
        {
          for (var j = 0; j < n; j++)
          {
            matrix[i, j] = dfs[i][b].ScalarProduct(fs[j]) + dfs[j][b].ScalarProduct(fs[i]);
          }
          vector[i] = ys.ScalarProduct(dfs[i][b]);
        }
        var matrixInverse = matrix.Inverse();
        var result = matrixInverse * vector;
        results.Add(result);
      }

      Func<double, DenseVector> gradient = x => new DenseVector(new[]
                                              {
                                                DotProduct(results[0], _l.Functions)(x),
                                                DotProduct(results[1], _l.Functions)(x),
                                                0//DotProduct(results[2], _l.Functions)(x)
                                              });

      return gradient;
    }

    private Func<double, double> DotProduct(Vector<double> coefficients, List<Func<double, double>> functions)
    {
      Func<double, double> result = x => 0;
      for (var j = 0; j < coefficients.Count; j++)
      {
        var result1 = result;
        var j1 = j;
        result = x => result1(x) + coefficients[j1] * functions[j1](x);
      }
      return result;
    }
  }
}
