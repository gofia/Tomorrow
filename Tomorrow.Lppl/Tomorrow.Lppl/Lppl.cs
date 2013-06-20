using System;
using System.Collections.Generic;
using Tomorrow.Mathematics;

namespace Tomorrow.Lppl
{
  public class Lppl: IFunction
  {
    public double A { get; set; }
    public double B { get; set; }
    public double C1 { get; set; }
    public double C2 { get; set; }
    public double Tc { get; set; }
    public double M { get; set; }
    public double Omega { get; set; }

    public double C
    {
      get { return Math.Sqrt(C1 * C1 + C2 * C2); }
    }

    public double Phi
    {
      get { return Math.Atan(C2 / C1); }
    }

    public List<Func<double, double>> Functions = new List<Func<double, double>>();

    public Lppl()
    {
      A = 4;
      B = -1;
      C1 = 0.5;
      C2 = 0.5;
      Tc = 1;
      M = 0.5;
      Omega = 10;

      Functions.Add(x => 1);
      Functions.Add(F);
      Functions.Add(G);
      Functions.Add(H);
    }

    public double Value(double t)
    {
      var deltaT = Tc - t;
      var powerFactor = Math.Pow(deltaT, M);
      var result = A + B * powerFactor
        + C * powerFactor * Math.Cos(Omega * Math.Log(deltaT) - Phi);

      if (double.IsNaN(result))
      {
        throw new Exception(String.Format("Lppl {0} is NaN in t = {1}.", this, t));
      }

      return result;
    }

    public double F(double t)
    {
      var deltaT = Tc - t;
      return Math.Pow(deltaT, M);
    }

    public double G(double t)
    {
      var deltaT = Tc - t;
      return F(t) * Math.Cos(Omega * Math.Log(deltaT));
    }

    public double H(double t)
    {
      var deltaT = Tc - t;
      return F(t) * Math.Sin(Omega * Math.Log(deltaT));
    }

    public override string ToString()
    {
      return String.Format(" A = {0}\n B = {1}\n C1 = {2}\n " +
                           "C2 = {3}\n Tc = {4}\n m = {5}\n " +
                           "Omega = {6}\n C = {7}\n Phi = {8}\n",
                           A, B, C1, C2, Tc, M, Omega, C, Phi);
    }

    public IDictionary<string, Parameter> Parameters { get; private set; }

    public bool HasParameter(string name)
    {
      throw new NotImplementedException();
    }

    public double Evaluate(double x)
    {
      return Value(x);
    }

    public List<double> Evaluate(List<double> xs)
    {
      throw new NotImplementedException();
    }

    public IFunction Derivative(string parameterName = "x")
    {
      throw new NotImplementedException();
    }

    public List<IFunction> ParameterDerivatives()
    {
      throw new NotImplementedException();
    }
  }
}
