using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

using MathNet.Numerics.LinearAlgebra.Double;

namespace Tomorrow.Lppl
{
  public class LpplLinearOptimizer
  {
    private readonly Lppl _lppl;

    public LpplLinearOptimizer(Lppl lppl)
    {
      _lppl = lppl;
    }

    public void Optimize(Dictionary<double, double> values)
    {
      var ys = new List<double>();
      var fs = new List<double>();
      var gs = new List<double>();
      var hs = new List<double>();

      foreach (var value in values)
      {
        ys.Add(value.Value);
        fs.Add(_lppl.F(value.Key));
        gs.Add(_lppl.G(value.Key));
        hs.Add(_lppl.H(value.Key));
      }

      var N = values.Count;
      var sfs = fs.Sum();
      var sgs = gs.Sum();
      var shs = hs.Sum();
      var sfsfs = fs.ScalarProduct(fs);
      var sgsgs = gs.ScalarProduct(gs);
      var shshs = hs.ScalarProduct(hs);
      var sfsgs = fs.ScalarProduct(gs);
      var sfshs = fs.ScalarProduct(hs);
      var sgshs = gs.ScalarProduct(hs);

      var sys = ys.Sum();
      var sysfs = ys.ScalarProduct(fs);
      var sysgs = ys.ScalarProduct(gs);
      var syshs = ys.ScalarProduct(hs);

      var matrixArray = new[]
                          {
                            N, sfs, sgs, shs,
                            sfs, sfsfs, sfsgs, sfshs,
                            sgs, sfsgs, sgsgs, sgshs,
                            shs, sfshs, sgshs, shshs
                          };

      var matrix = new DenseMatrix(4, 4, matrixArray);

      var matrixInverse = matrix.Inverse();

      var vector = new DenseVector(new[] { sys, sysfs, sysgs, syshs });

      var result = matrixInverse * vector;
      _lppl.A = result[0];
      _lppl.B = result[1];
      _lppl.C1 = result[2];
      _lppl.C2 = result[3];
    }
  }
}
