using System;
using System.Collections.Generic;
using MathNet.Numerics.LinearAlgebra.Double;
using Tomorrow.Mathematics;

namespace Tomorrow.Lppl2
{
  public class LcFunctionNonLinearOptimizer
  {
    private readonly LcFunction _lcf;
    private ConstraintLcFunction _clcf;

    public LcFunctionNonLinearOptimizer(LcFunction lcf)
    {
      _lcf = lcf;
    }

    public void Optimize(Dictionary<double, double> values)
    {
      _clcf = new ConstraintLcFunction(_lcf, values);

      var costFunction = new CostFunction(_clcf, values);
      var lastCost = costFunction.Evaluate();
      var costs = new List<double>();

      var expectedStepSize = 0.01;
      var setpsSinceLastChange = 0;
      var stepsSinceDecrease = 0;

      do
      {
        costs.Add(lastCost);

        var gradient = costFunction.Gradient();

        var norm = Math.Sqrt(gradient.ScalarProduct(gradient));
        var stepSize = - expectedStepSize / norm;

        _clcf.AddToB(stepSize.ScalarProduct(gradient));

        double cost = costFunction.Evaluate();

        if (lastCost - cost < 0 && stepsSinceDecrease > 5)
        {
          Console.WriteLine("DECREASE STEP SIZE:" + expectedStepSize);
          expectedStepSize /= 2.0;
          setpsSinceLastChange++;
          stepsSinceDecrease = 0;
        }
        else if (Math.Abs(lastCost - cost) < 10E-15)
        {
          break;
        }
        lastCost = cost;

        Console.WriteLine(cost);
        Console.WriteLine(gradient.ListToString());
        stepsSinceDecrease++;
      } while (setpsSinceLastChange < 20);

      Console.WriteLine(costs.ToListPlot());
    }
  }
}
