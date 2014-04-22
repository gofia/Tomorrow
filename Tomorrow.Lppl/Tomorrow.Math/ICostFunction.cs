using System.Collections.Generic;
using MathNet.Numerics.LinearAlgebra.Double;

namespace Tomorrow.Mathematics
{
  public interface ICostFunction
  {
    double Evaluate(Dictionary<double, double> values);
    DenseVector Gradient(Dictionary<double, double> values);
  }
}
