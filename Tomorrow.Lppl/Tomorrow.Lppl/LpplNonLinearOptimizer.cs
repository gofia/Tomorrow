using System;
using System.Collections.Generic;
using MathNet.Numerics.LinearAlgebra.Double;
using Tomorrow.Mathematics;

namespace Tomorrow.Lppl
{
  public class LpplNonLinearOptimizer
  {
    private readonly Lppl _lppl;
    private LpplGradient _lpplGradient;

    public LpplNonLinearOptimizer(Lppl lppl)
    {
      _lppl = lppl;
    }

    public void Optimize(Dictionary<double, double> values)
    {
      var costFunction = new SquareCostFunction(_lppl);
      var lastCost = 10E6;
      var cost = 0.0;
      var costs = new List<double>();

      _lpplGradient = new LpplGradient(_lppl, values);

      var setpsSinceLastChange = 0;
      var maxNorm = 10E6;

      double stepSize = 10E-5;

      do
      {
        var gradient = new DenseVector(3, 0.0);

        foreach (var value in values)
        {
          var t = value.Key;
          var deltaValue = value.Value - _lppl.Value(t);
          gradient += - _lpplGradient.Gradient(t) * deltaValue;
        }

        _lppl.M -= gradient[0] * stepSize;
        _lppl.Omega -= gradient[1] * stepSize;
        _lppl.Tc -= gradient[2] * stepSize;

        var optimizer = new LpplLinearOptimizer(_lppl);
        optimizer.Optimize(values);

        cost = costFunction.Evaluate(values);
        costs.Add(costFunction.Evaluate(values));

        if (lastCost - cost < 0)
        {
          stepSize /= 2.0;
          setpsSinceLastChange++;
        }
        lastCost = cost;

        //var norm = gradient.Norm(1);
        //if (norm < maxNorm)
        //{
        //  maxNorm = norm;
        //  setpsSinceLastChange = 0;
        //}
        Console.WriteLine(cost);
        Console.WriteLine(gradient);
      } while (setpsSinceLastChange < 2);

      Console.WriteLine(costs.ToListPlot());
    }
  }
}
