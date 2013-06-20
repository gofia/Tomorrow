using System;

namespace Tomorrow.Lppl2
{
  public class Lppl : LcFunction
  {
    public Lppl()
    {
      AddB(1);
      AddB(0.5);
      AddB(10);

      AddFunction(4, x => 1);
      AddFunction(-1, x => Math.Pow(B(0) - x, B(1)));
      AddFunction(0.5, x => Math.Pow(B(0) - x, B(1)) * Math.Cos(B(2) * Math.Log(B(0) - x)));
      AddFunction(0.5, x => Math.Pow(B(0) - x, B(1)) * Math.Sin(B(2) * Math.Log(B(0) - x)));
    }

    public new double A
    {
      get { return A(0); }
      set { SetA(0, value); }
    }

    public new double B
    {
      get { return A(1); }
      set { SetA(1, value); }
    }

    public double C1
    {
      get { return A(2); }
      set { SetA(2, value); }
    }

    public double C2
    {
      get { return A(3); }
      set { SetA(3, value); }
    }

    public double Tc
    {
      get { return B(0); }
      set { SetB(0, value); }
    }

    public double M
    {
      get { return B(1); }
      set { SetB(1, value); }
    }

    public double Omega
    {
      get { return B(2); }
      set { SetB(2, value); }
    }

    public double C
    {
      get { return Math.Sqrt(C1 * C1 + C2 * C2); }
    }

    public double Phi
    {
      get { return Math.Atan(C2 / C1); }
    }

    public override string ToString()
    {
      return String.Format(" A = {0}\n B = {1}\n C1 = {2}\n " +
                           "C2 = {3}\n Tc = {4}\n m = {5}\n " +
                           "Omega = {6}\n C = {7}\n Phi = {8}\n",
                           A, B, C1, C2, Tc, M, Omega, C, Phi);
    }
  }
}
