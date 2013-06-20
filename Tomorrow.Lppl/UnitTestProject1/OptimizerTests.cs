using System;
using NUnit.Framework;

namespace Tomorrow.Lppl2.Tests
{
  [TestFixture]
  public class OptimizerTests
  {
    [Test]
    public void TestLinearOptimizePl()
    {
      var pl = new Pl();

      var options = new GeneratorOptions
      {
        Function = pl.Evaluate,
        ErrorRange = 0.25
      };
      var generator = new Generator(options);
      var generated = generator.Generate();

      var optimizer = new LcFunctionLinearOptimizer(pl);
      optimizer.Optimize(generated);
      Console.WriteLine(pl.ToShow(generated));
    }

    [Test]
    public void TestNonLinearOptimizePl()
    {
      var pl = new Pl();
      Console.WriteLine(pl);

      var options = new GeneratorOptions
      {
        Function = pl.Evaluate,
        ErrorRange = 0,//.1,
        TimeRangeMax = 0.8
      };
      var generator = new Generator(options);
      var generated = generator.Generate();

      pl.Tc += 0.5;// 5;
      pl.M += 0.3;

      var optimizer = new LcFunctionNonLinearOptimizer(pl);
      optimizer.Optimize(generated);
      Console.WriteLine(pl);
      Console.WriteLine(pl.ToShow(generated));
    }

    [Test]
    public void TestLinearOptimizeLppl()
    {
      var lppl = new Lppl();

      var options = new GeneratorOptions
                      {
                        Function = lppl.Evaluate,
                        ErrorRange = 0.25
                      };
      var generator = new Generator(options);
      var generated = generator.Generate();

      var optimizer = new LcFunctionLinearOptimizer(lppl);
      optimizer.Optimize(generated);
      Console.WriteLine(lppl.ToShow(generated));
    }

    [Test]
    public void TestNonLinearOptimizeLppl()
    {
      var lppl = new Lppl();

      var options = new GeneratorOptions
      {
        Function = lppl.Evaluate,
        TimeRangeMax = 0.9,
        ErrorRange = 0.1
      };
      var generator = new Generator(options);
      var generated = generator.Generate();

      lppl.M += 0.0;
      lppl.Omega -= 0.5;
      lppl.Tc += 0.0;

      var optimizer = new LcFunctionNonLinearOptimizer(lppl);
      optimizer.Optimize(generated);
      Console.WriteLine(lppl);
      Console.WriteLine(lppl.ToShow(generated));
    }
  }
}
