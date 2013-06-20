using System;
using System.Collections.Generic;

namespace Tomorrow.Lppl
{
  public class LpplGenerator
  {
    public LpplGenerator(LpplGeneratorOptions options)
    {
      Options = options;
    }

    public LpplGeneratorOptions Options { get; set; }

    public Dictionary<double, double> Generate()
    {
      var t = Options.TimeRangeMin;
      var result = new Dictionary<double, double>();
      var random = new Random(DateTime.Now.Millisecond);
      
      while (t < Options.TimeRangeMax)
      {
        var value = Options.Lppl.Value(t);
        value += (0.5 - random.NextDouble()) * 2 * Options.ErrorRange;
        result.Add(t, value);
        t += Options.TimeSteps;
      }

      return result;
    } 
  }
}
