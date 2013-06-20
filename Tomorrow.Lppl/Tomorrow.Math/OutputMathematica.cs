using System;
using System.Collections.Generic;
using System.Linq;

namespace Tomorrow.Mathematics
{
  public static class OutputMathematica
  {
    public static string ToListPlot(this List<double> plot)
    {
      var result = "ListPlot[" + plot.ListToString() + "]";
      return result;
    }

    public static string ListToString(this List<double> plot)
    {
      var result = String.Join(",", plot);
      result = "{" + result + "}";
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
