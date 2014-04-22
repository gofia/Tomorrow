using System;
using System.Collections.Generic;

namespace Tomorrow.Lppl2
{
  public class ConstraintLcFunction
  {
    private readonly LcFunction _f;
    private readonly LcFunctionLinearOptimizer _linearOptimizer;

    public ConstraintLcFunction(LcFunction f, Dictionary<double, double> values)
    {
      _f = f;
      _linearOptimizer = new LcFunctionLinearOptimizer(f, values);
    }

    public int NonLinearCount
    {
      get { return _f.NonLinearCount; }
    }

    public double Evaluate(double x)
    {
      return _f.Evaluate(x);
    }

    /// <summary>
    /// Sets the nth non linear parameter.
    /// </summary>
    /// <param name="n">Non linear parameter index.</param>
    /// <returns>Non linear parameter value.</returns>
    public double B(int n)
    {
      return _f.B(n);
    }

    /// <summary>
    /// Gets the nth non linear parameter.
    /// </summary>
    /// <param name="n">Non linear parameter index.</param>
    /// <param name="value">Value.</param>
    /// <returns>Non linear parameter value.</returns>
    public void SetB(int n, double value)
    {
      _f.SetB(n, value);
      _linearOptimizer.Optimize();
    }

    public void AddToB(int n, double value)
    {
      _f.AddToB(n, value);
      _linearOptimizer.Optimize();
    }

    public void AddToB(List<double> values)
    {
      if (values.Count != _f.NonLinearCount)
      {
        throw new Exception(
          String.Format("There are {0} non linear parameters.", _f.NonLinearCount));
      }

      for (var i = 0; i < _f.NonLinearCount; i++)
      {
        _f.AddToB(i, values[i]);
      }

      _linearOptimizer.Optimize();
    }

    public List<double> ParameterGradient(double x)
    {
      var gradient = new List<double>();
      for (int i = 0; i < NonLinearCount; i++)
      {
        gradient.Add(ParameterGradient(i, x));
      }
      return gradient;
    }

    private double ParameterGradient(int n, double x)
    {
      const double h = 10E-6;
      AddToB(n, h);
      var fph = _f.Evaluate(x);
      AddToB(n, -2 * h);
      var fmh = _f.Evaluate(x);
      AddToB(n, h);
      var derivative = (fph - fmh) / (2 * h);
      return derivative;
    }
  }
}
