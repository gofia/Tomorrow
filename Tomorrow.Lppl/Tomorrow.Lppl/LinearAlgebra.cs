using System;
using System.Collections.Generic;

namespace Tomorrow.Lppl
{
  public static class LinearAlgebra
  {
    public static double ScalarProduct(this List<double> a, List<double> b)
    {
      var result = 0.0;
      var length = Math.Max(a.Count, b.Count);
      for (var i = 0; i < length; i++)
      {
        result += a[i]*b[i];
      }
      return result;
    }
  }
}
