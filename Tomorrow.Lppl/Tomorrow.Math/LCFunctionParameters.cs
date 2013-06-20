using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Tomorrow.Mathematics
{
  public class LCFunctionParameters
  {
    public List<Parameter> A { get; set; }
    public List<IFunction> F { get; set; }
    public List<Parameter> B { get; set; }

    public void Validate()
    {
      var valid = A.Count == F.Count;
      
      if (!valid)
      {
        throw new Exception("LCFunctionParameters are invalid.");
      }
    }
  }
}
