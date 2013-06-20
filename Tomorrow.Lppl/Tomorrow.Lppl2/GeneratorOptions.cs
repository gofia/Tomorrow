using System;

namespace Tomorrow.Lppl2
{
  public class GeneratorOptions
  {
    public GeneratorOptions()
    {
      Function = x => new Lppl().Evaluate(x);
      TimeRangeMin = 0.1;
      TimeRangeMax = 0.99;
      TimeSteps = 0.01;
      ErrorRange = 0.1;
    }

    public Func<double, double> Function { get; set; }
    public double TimeRangeMin { get; set; }
    public double TimeRangeMax { get; set; }
    public double TimeSteps { get; set; }
    public double ErrorRange { get; set; }
  }
}
