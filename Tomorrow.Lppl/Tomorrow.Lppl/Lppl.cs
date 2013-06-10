using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Tomorrow.Lppl
{
  public class Lppl
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

    public Lppl()
    {
      A = 1;
      B = -1;
      C1 = 0.5;
      C2 = 0.5;
      Tc = 1;
      M = 0.5;
      Omega = 10;
    }

    public double Value(double t)
    {
      var deltaT = Tc - t;
      var powerFactor = Math.Pow(deltaT, M);
      return A + B * powerFactor + C * powerFactor * Math.Cos(Omega * Math.Log(deltaT) - Phi);
    }

    public double F(double t)
    {
      var deltaT = Tc- t;
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
  }
}
