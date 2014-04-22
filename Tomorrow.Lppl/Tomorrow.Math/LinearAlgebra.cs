using System;
using System.Collections.Generic;
using System.Linq;

namespace Tomorrow.Mathematics
{
  public static class LinearAlgebra
  {
    public static double ScalarProduct(this List<double> a, List<double> b)
    {
      var result = 0.0;
      var length = Math.Min(a.Count, b.Count);
      for (var i = 0; i < length; i++)
      {
        result += a[i] * b[i];
      }
      return result;
    }

    public static List<double> ScalarProduct(this double a, List<double> b)
    {
      return b.Select(t => a*t).ToList();
    }

    public static List<double> ScalarProduct(this List<double> a, List<List<double>> b)
    {
      var result = new List<double>(a[0].ScalarProduct(b[0]));
      var length = Math.Min(a.Count, b.Count);
      for (var i = 1; i < length; i++)
      {
        result.Sum(a[i].ScalarProduct(b[i]));
      }
      return result;
    }

    public static List<double> Sum(this List<double> a, List<double> b)
    {
      var result = new List<double>();
      var length = Math.Min(a.Count, b.Count);
      for (var i = 0; i < length; i++)
      {
        result.Add(a[i] + b[i]);
      }
      return result;
    }
  }
}
