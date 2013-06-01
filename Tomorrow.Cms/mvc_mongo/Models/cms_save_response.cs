using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;

using MongoDB.Bson;

namespace mvc_mongo.Models
{
  /// <summary>
  /// A cms response for a given cms parameter.
  /// </summary>
  /// <typeparam name="T">Id type.</typeparam>
  public class cms_save_response
  {
    /// <summary>
    /// Create a new instance.
    /// </summary>
    /// <param name="parameter">Cms parameter.</param>
    public cms_save_response()
    {
      id = new ObjectId();
      success = false;
      message = string.Empty;
    }

    /// <summary>
    /// Indicates if the cms action was successful.
    /// </summary>
    public ObjectId id { get; set; }
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