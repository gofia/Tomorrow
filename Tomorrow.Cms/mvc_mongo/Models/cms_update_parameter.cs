using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;

using MongoDB.Bson;

namespace mvc_mongo.Models
{
  public class cms_update_parameter
  {
    public cms_update_parameter() { }

    public string collection { get; set; }
    public ObjectId id { get; set; }
    public string field { get; set; }
    public string language { get; set; }
    public BsonValue value { get; set; }
  }
}