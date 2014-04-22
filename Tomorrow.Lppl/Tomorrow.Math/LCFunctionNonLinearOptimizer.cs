using System;
using System.Collections.Generic;
using System.Linq;
using MathNet.Numerics.LinearAlgebra.Double;
using MathNet.Numerics.LinearAlgebra.Generic;
using Tomorrow.Mathematics;

namespace Tomorrow.Mathematics
{
  public class LpplNonLinearOptimizer
  {
    private readonly LCFunction _f;

    public LpplNonLinearOptimizer(LCFunction f)
    {
      _f = f;
    }

    public void Optimize(Dictionary<double, double> values)
    {
      

      //for (var i = 0; i < n; i++)
      //{
      //  _f.LinearParameters[i].Value = result[i];
      //}

      ////-------------------------------------------------------------

      //var setpsSinceLastChange = 0;
      //var maxNorm = 10E6;

      //do
      //{
      //  setpsSinceLastChange++;
      //  var gradient = new DenseVector(3, 0.0);

      //  foreach (var value in values)
      //  {
      //    var t = value.Key;
      //    var deltaValue = value.Value - _lppl.Value(t);
      //    gradient += _lpplGradient.Gradient(t) * deltaValue;
      //  }

      //  const double stepSize = 0.0005;

      //  _lppl.M -= gradient[0] * stepSize;
      //  _lppl.Omega -= gradient[1] * stepSize;
      //  _lppl.Tc -= gradient[2] * stepSize;

      //  var optimizer = new LpplLinearOptimizer(_lppl);
      //  optimizer.Optimize(values);

      //  var norm = gradient.Norm(1);
      //  if (norm < maxNorm)
      //  {
      //    maxNorm = norm;
      //    setpsSinceLastChange = 0;
      //  }

      //  Console.WriteLine(gradient);
      //} while (setpsSinceLastChange < 20);
    }

    //private DenseVector NonLinearParameterGradient(Dictionary<double, double> values)
    //{
    //  var nb = _f.NonLinearParameters.Count;
    //  var gradient = new DenseVector(nb, 0.0);

    //  var n = _f.Functions.Count();
    //  var xs = values.Select(v => v.Key).ToList();
    //  var ys = values.Select(v => v.Value).ToList();
    //  var fs = new List<List<double>>(n);
    //  var dfs = new List<List<List<double>>>(n);

    //  for (var i = 0; i < n; i++)
    //  {
    //    var function = _f.Functions[i];
    //    fs[i] = function.Evaluate(xs);
    //    var derivatives = function.ParameterDerivatives();
    //    for (var j = 0; j < nb; j++)
    //    {
    //      dfs[i][j].Add(derivatives[j].Evaluate(xs));
    //    }
    //  }

    //  var sfs = new DenseVector(fs.Select(f => f.Sum()).ToArray());

    //  for (var b = 0; b < nb; b++)
    //  {
    //    var matrix = new DenseMatrix(n, n);
    //    var vector = new DenseVector(n);
    //    for (var i = 0; i < n; i++)
    //    {
    //      for (var j = 0; j < n; j++)
    //      {
    //        matrix[i, j] = dfs[i][b].ScalarProduct(fs[j]) + dfs[j][b].ScalarProduct(fs[i]);
    //      }
    //      vector[i] = ys.ScalarProduct(dfs[i][b]);
    //    }
    //    var matrixInverse = matrix.Inverse();
    //    var result = matrixInverse * vector;
    //    gradient[b] += result.DotProduct(sfs);
    //    var dbfs = dfs.Select(df => df[b]).ToArray()
    //  }

    //  return gradient;
    //}
  }
}
