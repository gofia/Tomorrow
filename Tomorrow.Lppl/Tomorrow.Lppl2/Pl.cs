using System;

namespace Tomorrow.Lppl2
{
  public class Pl : LcFunction
  {
    public Pl()
    {
      AddB(1);
      AddB(0.5);

      AddFunction(4, x => 1);
      AddFunction(-1, x => Math.Pow(B(0) - x, B(1)));
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

    public override string ToString()
    {
      return String.Format(" A = {0}\n B = {1}\n " +
                           "Tc = {2}\n m = {3}\n ",
                           A, B, Tc, M);
    }
  }
}
