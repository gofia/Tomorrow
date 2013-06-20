using System;
using System.Collections.Generic;
using System.Linq;

namespace Tomorrow.Lppl
{
  public static class OutputMathematica
  {
    public static string ToShow(this Lppl lppl, Dictionary<double, double> plot)
    {
      var result = String.Format("{0}\nShow[{1}, Plot[f[t], {{t, 0, 1}}]]", 
        lppl.ToFunction(), plot.ToListPlot());
      return result;
    }

    public static string ToFunction(this Lppl lppl)
    {
      var result = String.Format("f[t_] := {0} + " +
                                 "({6} - t)^{1} * ({2} + " +
                                 "{3}*Cos[{4} *Log[{6} - t] ] + " +
                                 "{5}*Sin[{4}*Log[{6} - t]]);",
                                 lppl.A, lppl.M, lppl.B, lppl.C1, lppl.Omega, lppl.C2, lppl.Tc);
      return result;
    }

    public static string ToListPlot(this List<double> plot)
    {
      var result = String.Join(",", plot);
      result = "{" + result + "}";
      result = "ListPlot[" + result + "]";
      return result;
    }

    public static string ToListPlot(this Dictionary<double, double> plot)
    {
      var temp = plot.Select(p => p.ToValuePair());
      var result = String.Join(",", temp);
      result = "{" + result + "}";
      result = "ListPlot[" + result + "]";
      return result;
    }

    public static string ToValuePair(this KeyValuePair<double, double> pair)
    {
      return String.Format("{{{0}, {1}}}", pair.Key, pair.Value);
    }
  }
}
