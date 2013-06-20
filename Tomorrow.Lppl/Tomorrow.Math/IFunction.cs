using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Tomorrow.Mathematics
{
  public interface IFunction
  {
    IDictionary<string, Parameter> Parameters { get; }
    bool HasParameter(string name);
    double Evaluate(double x);
    List<double> Evaluate(List<double> xs);
    IFunction Derivative(string parameterName = "x");
    List<IFunction> ParameterDerivatives();
  }
}
