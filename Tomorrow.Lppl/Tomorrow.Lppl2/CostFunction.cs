using System.Collections.Generic;
using System.Linq;
using Tomorrow.Mathematics;

namespace Tomorrow.Lppl2
{
  public class CostFunction
  {
    private readonly ConstraintLcFunction _cf;
    private readonly Dictionary<double, double> _values;

    public CostFunction(ConstraintLcFunction cf, Dictionary<double, double> values)
    {
      _cf = cf;
      _values = values;
    }

    public double Evaluate()
    {
      return Deltas.Select(temp => temp*temp).Sum();
    }

    public List<double> Gradient()
    {
      var fGradient = _values.Select(v => _cf.ParameterGradient(v.Key)).ToList();
      var deltas = Deltas.ToList();
      return (-2.0).ScalarProduct(deltas.ScalarProduct(fGradient));
    }

    private IEnumerable<double> Deltas
    {
      get { return _values.Select(value => value.Value - _cf.Evaluate(value.Key)); }
    } 
  }
}
