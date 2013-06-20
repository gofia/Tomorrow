using System;

using NUnit.Framework;
using Tomorrow.Mathematics;

namespace Tomorrow.Lppl2.Tests
{
  [TestFixture]
  public class GeneratorTests
  {
    [Test]
    public void TestGeneratePl()
    {
      var options = new GeneratorOptions
      {
        Function = x => new Pl().Evaluate(x)
      };
      var generator = new Generator(options);
      var generated = generator.Generate();
      Console.WriteLine(generated.ToListPlot());
    }

    [Test]
    public void TestGenerateLppl()
    {
      var options = new GeneratorOptions();
      var generator = new Generator(options);
      var generated = generator.Generate();
      Console.WriteLine(generated.ToListPlot());
    }
  }
}
