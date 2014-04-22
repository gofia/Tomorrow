using System;
using System.Collections.Generic;
using System.Linq;
using MathNet.Numerics.LinearAlgebra.Double;

namespace Tomorrow.Mathematics
{
  public class SquareCostFunction: ICostFunction
  {
    private readonly IFunction _f;

    public SquareCostFunction(IFunction f)
    {
      _f = f;
    }

    public double Evaluate(Dictionary<double, double> values)
    {
      return values
        .Select(value => value.Value - _f.Evaluate(value.Key))
        .Select(temp => temp*temp).Sum();
    }

    public DenseVector Gradient(Dictionary<double, double> values)
    {
      throw new NotImplementedException();
    }
  }
}
