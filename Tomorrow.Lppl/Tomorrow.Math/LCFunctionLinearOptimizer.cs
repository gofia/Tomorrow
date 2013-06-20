using System.Collections.Generic;
using System.Linq;
using MathNet.Numerics.LinearAlgebra.Double;

namespace Tomorrow.Mathematics
{
  public class LCFunctionLinearOptimizer
  {
    private readonly LCFunction _f;

    public LCFunctionLinearOptimizer(LCFunction f)
    {
      _f = f;
    }

    public void Optimize(Dictionary<double, double> values)
    {
      var n = _f.Functions.Count();
      var xs = values.Select(v => v.Key).ToList();
      var ys = values.Select(v => v.Value).ToList();
      var fs = new List<List<double>>(n);

      for (var i = 0; i < n; i++)
      {
        fs[i] = _f.Functions[i].Evaluate(xs);
      }

      var matrix = new DenseMatrix(n, n);
      var vector = new DenseVector(n);
      for (var i = 0; i < n; i++)
      {
        for (var j = 0; j < n; j++)
        {
          matrix[i, j] = fs[i].ScalarProduct(fs[j]);
        }
        vector[i] = ys.ScalarProduct(fs[i]);
      }

      var matrixInverse = matrix.Inverse();
      
      var result = matrixInverse * vector;

      for (var i = 0; i < n; i++)
      {
        _f.LinearParameters[i].Value = result[i];
      }
    }
  }
}
