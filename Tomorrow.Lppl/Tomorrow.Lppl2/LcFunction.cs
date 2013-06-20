using System;
using System.Collections.Generic;
using System.Linq;
using Tomorrow.Mathematics;

namespace Tomorrow.Lppl2
{
  /// <summary>
  /// Linear Combination Function
  /// A function which is a linear combination of functions.
  /// </summary>
  public abstract class LcFunction
  {
    private readonly List<double> _linearParameters = new List<double>();
    private readonly List<double> _nonLinearParameters = new List<double>();
    private readonly List<Func<double, double>> _functions = new List<Func<double, double>>();

    public int LinearCount
    {
      get { return _linearParameters.Count; }
    }

    public int NonLinearCount
    {
      get { return _nonLinearParameters.Count; }
    }

    public List<Func<double, double>> Functions
    {
      get { return _functions; }
    }

    public void AddFunction(double linearParameter, Func<double, double> function)
    {
      _linearParameters.Add(linearParameter);
      _functions.Add(function);
    }

    public double Evaluate(double x)
    {
      var fs = _functions.Select(f => f(x)).ToList();
      return _linearParameters.ScalarProduct(fs);
    }

    /// <summary>
    /// Gets the nth linear parameter.
    /// </summary>
    /// <param name="n">Linear parameter index.</param>
    /// <returns>Linear parameter value.</returns>
    public double A(int n)
    {
      if (n >= _linearParameters.Count)
      {
        throw new Exception(String.Format("Linear parameter {0} does not exist.", n));
      }

      return _linearParameters[n];
    }

    /// <summary>
    /// Sets the nth linear parameter.
    /// </summary>
    /// <param name="n">Linear parameter index.</param>
    /// <param name="value">Value.</param>
    /// <returns>Linear parameter value.</returns>
    public void SetA(int n, double value)
    {
      if (n >= _linearParameters.Count)
      {
        throw new Exception(String.Format("Linear parameter {0} does not exist.", n));
      }

      if (double.IsNaN(value))
      {
        throw new Exception(String.Format("Value Nan is not permitted."));
      }

      _linearParameters[n] = value;
    }

    protected void AddB(double value)
    {
      _nonLinearParameters.Add(value);
    }

    /// <summary>
    /// Sets the nth non linear parameter.
    /// </summary>
    /// <param name="n">Non linear parameter index.</param>
    /// <returns>Non linear parameter value.</returns>
    public double B(int n)
    {
      if (n >= _nonLinearParameters.Count)
      {
        throw new Exception(String.Format("Non linear parameter {0} does not exist.", n));
      }

      return _nonLinearParameters[n];
    }

    /// <summary>
    /// Gets the nth non linear parameter.
    /// </summary>
    /// <param name="n">Non linear parameter index.</param>
    /// <param name="value">Value.</param>
    /// <returns>Non linear parameter value.</returns>
    public void SetB(int n, double value)
    {
      if (n >= _nonLinearParameters.Count)
      {
        throw new Exception(String.Format("Linear parameter {0} does not exist.", n));
      }

      if (double.IsNaN(value))
      {
        throw new Exception(String.Format("Value Nan is not permitted."));
      }

      _nonLinearParameters[n] = value;
    }

    public void AddToB(int n, double delta)
    {
      if (n >= _nonLinearParameters.Count)
      {
        throw new Exception(String.Format("Linear parameter {0} does not exist.", n));
      }

      _nonLinearParameters[n] += delta;
    }
  }
}
