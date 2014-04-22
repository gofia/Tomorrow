using System;
using System.Collections.Generic;
using Tomorrow.Mathematics;

namespace Tomorrow.Lppl2
{
  public static partial class OutputMathematica
  {
    public static string ToShow(this Pl pl, Dictionary<double, double> plot)
    {
      var result = String.Format("{0}\nShow[{1}, Plot[f[t], {{t, 0, 1}}]]",
        pl.ToFunction(), plot.ToListPlot());
      return result;
    }

    public static string ToFunction(this Pl pl)
    {
      var result = String.Format("f[t_] := {0} + {2} * ({3} - t)^{1}",
                                 pl.A, pl.M, pl.B, pl.Tc);
      return result;
    }

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
  }
}
