using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;

namespace mvc_mongo.Models
{
  /// <summary>
  /// A cms response for a given cms parameter.
  /// </summary>
  /// <typeparam name="T">Id type.</typeparam>
  public class cms_update_response: cms_update_parameter
  {
    /// <summary>
    /// Create a new instance.
    /// </summary>
    /// <param name="parameter">Cms parameter.</param>
    public cms_update_response(cms_update_parameter parameter)
    {
      collection = parameter.collection;
      id = parameter.id;
      field = parameter.field;
      language = parameter.language;
      value = parameter.value;
      success = false;
      message = string.Empty;
    }

    /// <summary>
    /// Indicates if the cms action was successful.
    /// </summary>
    public bool success { get; set; }
    /// <summary>
    /// An eventual message concerning the cms action.
    /// </summary>
    public string message { get; set; }
  }
}