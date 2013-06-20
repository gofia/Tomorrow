using System;
using System.Collections.Generic;
using System.Linq;

namespace Tomorrow.Mathematics
{
  /// <summary>
  /// Linear combination function
  /// </summary>
  public class LCFunction : IFunction
  {
    private readonly LCFunctionParameters _parameters;

    public LCFunction(LCFunctionParameters parameters)
    {
      parameters.Validate();
      _parameters = parameters;
    }

    public IDictionary<string, Parameter> Parameters
    {
      get
      {
        return _parameters.A.Concat(_parameters.B).ToDictionary(p => p.Name);
      }
    }

    public List<Parameter> LinearParameters
    {
      get
      {
        return _parameters.A;
      }
    }

    public List<Parameter> NonLinearParameters
    {
      get
      {
        return _parameters.B;
      }
    }

    public List<IFunction> Functions
    {
      get
      {
        return _parameters.F;
      }
    }

    public bool HasParameter(string name)
    {
      return Parameters.ContainsKey(name);
    }

    public double Evaluate(double x)
    {
      var value = _parameters.A.Select((t, i) => t.Value * _parameters.F[i].Evaluate(x)).Sum();
      return value;
    }

    public List<double> Evaluate(List<double> xs)
    {
      return xs.Select(Evaluate).ToList();
    }

    public IFunction Derivative(string parameter = "x")
    {
      throw new NotImplementedException();
    }

    public List<IFunction> ParameterDerivatives()
    {
      throw new NotImplementedException();
    }

    public IFunction Derivative(uint index, string name)
    {
      if (index >= _parameters.F.Count)
      {
        throw new Exception();
      }

      var function = _parameters.F[(int)index];

      if (!function.HasParameter(name))
      {
        throw new Exception();
      }

      return function.Derivative(name);
    }
  }
}
