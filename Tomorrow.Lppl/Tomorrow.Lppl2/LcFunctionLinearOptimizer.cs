using System.Collections.Generic;
using System.Linq;
using MathNet.Numerics.LinearAlgebra.Double;
using Tomorrow.Mathematics;

namespace Tomorrow.Lppl2
{
  public class LcFunctionLinearOptimizer
  {
    private readonly LcFunction _f;
    private readonly Dictionary<double, double> _values;

    public LcFunctionLinearOptimizer(LcFunction f)
    {
      _f = f;
    }
    public LcFunctionLinearOptimizer(LcFunction f, Dictionary<double, double> values)
    {
      _f = f;
      _values = values;
    }

    public void Optimize()
    {
      Optimize(_values);
    }

    public void Optimize(Dictionary<double, double> values)
    {
      var ys = values.Select(v => v.Value).ToList();
      var fs = _f.Functions.Select(f => values.Select(v => NaNToZero(f(v.Key))).ToList()).ToList();

      var matrix = new DenseMatrix(_f.LinearCount, _f.LinearCount);
      var vector = new DenseVector(_f.LinearCount);
      for (var i = 0; i < _f.LinearCount; i++)
      {
        for (var j = 0; j < _f.LinearCount; j++)
        {
          matrix[i, j] = fs[i].ScalarProduct(fs[j]);
        }
        vector[i] = ys.ScalarProduct(fs[i]);
      }

      var matrixInverse = matrix.Inverse();
      var result = matrixInverse * vector;
      
      for (var i = 0; i < _f.LinearCount; i++)
      {
        _f.SetA(i, result[i]);
      }
    }

    private double NaNToZero(double x)
    {
      return double.IsNaN(x) ? 0 : x;
    }
  }
}
