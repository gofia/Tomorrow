namespace Tomorrow.Mathematics
{
  public class Parameter
  {
    public string Name { get; set; }
    public double Value { get; set; }

    public Parameter(string name, double value)
    {
      Name = name;
      Value = value;
    }

    public bool Equals(Parameter p)
    {
      // If parameter is null return false:
      if (p == null)
      {
        return false;
      }

      // Return true if the fields match:
      return (Name == p.Name) && (Value == p.Value);
    }
  }
}
