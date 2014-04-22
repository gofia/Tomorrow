using System;
using System.Collections.Generic;

namespace Tomorrow.Lppl2
{
  public class Generator
  {
    public Generator(GeneratorOptions options)
    {
      Options = options;
    }

    public GeneratorOptions Options { get; set; }

    public Dictionary<double, double> Generate()
    {
      var t = Options.TimeRangeMin;
      var result = new Dictionary<double, double>();
      var random = new Random(DateTime.Now.Millisecond);
      
      while (t < Options.TimeRangeMax)
      {
        var value = Options.Function(t);
        value += (0.5 - random.NextDouble()) * 2 * Options.ErrorRange;
        result.Add(t, value);
        t += Options.TimeSteps;
      }

      return result;
    } 
  }
}
