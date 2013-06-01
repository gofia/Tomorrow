using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;

namespace mvc_mongo.Models
{
  public static class cms_configuration
  {
    static cms_configuration()
    {
      debug = true;
      language = "EN";
    }

    public static bool debug { get; set; }
    public static string language { get; set; }
    public static IEnumerable<string> languages
    {
      get
      {
        return new List<string> { "EN", "DE", "FR" };
      }
    }
  }
}