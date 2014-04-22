using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;

using MongoDB.Bson;

namespace mvc_mongo.Models
{
  public static class bson_extensions
  {
    public static void OrderFields(this BsonDocument document)
    {
      var documentClone = document.DeepClone();
      document.Clear();

      var names = document.Names.ToList();
      names.Sort();

      foreach (var field in document)
      {
        var name = field.Name;
        var index = names.IndexOf(name);
        document.Add(name, field.Value);
      }
    }

    public static BsonValue Current(this BsonValue value)
    {
      return value.Current(cms_configuration.language);
    }

    public static BsonValue Current(this BsonValue value, string language)
    {
      if (value.IsBsonDocument)
      {
        var document = value.AsBsonDocument;
        value = document.Current(language);
        return value;
      }

      if (value.IsBsonArray)
      {
        var array = value.AsBsonArray;
        value = array.Current(language);
        return value;
      }

      return value;
    }

    public static IEnumerable<BsonDocument> Current(this IEnumerable<BsonDocument> documents)
    {
      return documents.Current(cms_configuration.language);
    }

    public static IEnumerable<BsonDocument> Current(this IEnumerable<BsonDocument> documents, 
      string language)
    {
      ICollection<BsonDocument> currentDocuments = new List<BsonDocument>();
      foreach (var d in documents)
      {
        currentDocuments.Add(d.Current().AsBsonDocument);
      }
      return currentDocuments;
    }

    public static BsonValue Current(this BsonDocument document)
    {
      return document.Current(cms_configuration.language);
    }

    public static BsonValue Current(this BsonDocument document, string language)
    {
      var keys = document.Names;
      if (keys.Contains(language))
      {
        var value = document[language];
        var currentValue = value.Current(language);
        return currentValue;
      }

      if (keys.Count() == 2 && keys.Contains("Date") && keys.Contains("Value"))
      {
        var currentValue = document["Value"];
        return currentValue;
      }

      foreach (var field in document)
      {
        var value = field.Value;
        var currentValue = value.Current(language);
        document[field.Name] = currentValue;
      }

      return document;
    }

    public static BsonValue Current(this BsonArray array)
    {
      return array.Current(cms_configuration.language);
    }

    public static BsonValue Current(this BsonArray array, string language)
    {
      try
      {
        var value = array.OrderByDescending(v => v.AsBsonDocument["Date"]);
        var first = value.First();
        var currentValue = first.Current(language);
        return currentValue;
      }
      catch (Exception e)
      {
        return array;
      }
    }
  }
}