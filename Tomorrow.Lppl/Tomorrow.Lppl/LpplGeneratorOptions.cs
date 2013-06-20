namespace Tomorrow.Lppl
{
  public class LpplGeneratorOptions
  {
    public LpplGeneratorOptions()
    {
      Lppl = new Lppl();
      TimeRangeMin = 0.1;
      TimeRangeMax = 0.99;
      TimeSteps = 0.01;
      ErrorRange = 0.1;
    }

    public Lppl Lppl { get; set; }
    public double TimeRangeMin { get; set; }
    public double TimeRangeMax { get; set; }
    public double TimeSteps { get; set; }
    public double ErrorRange { get; set; }
  }
}
