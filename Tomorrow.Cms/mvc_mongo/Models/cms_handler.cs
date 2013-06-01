using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;

using MongoDB.Bson;
using MongoDB.Driver;
using MongoDB.Driver.Builders;

namespace mvc_mongo.Models
{
  public class cms_handler: icms_handler
  {
    private MongoDatabase _db;

    public cms_handler(MongoDatabase db)
    {
      _db = db;
    }

    public cms_save_response save(string collectionName, BsonDocument document)
    {
      return save(collectionName, new List<BsonDocument> { document }).Single();
    }

    public IEnumerable<cms_save_response> save(string collectionName, 
      IEnumerable<BsonDocument> documents)
    {
      var responses = new List<cms_save_response>();
      IEnumerable<WriteConcernResult> results = new List<WriteConcernResult>();

      try
      {
        var collection = _db.GetCollection(collectionName);
        results = collection.InsertBatch(documents);
        foreach (var r in results)
        {
          var response = new cms_save_response();
          var index = results.ToList().IndexOf(r);
          var document = documents.ToList()[index];
          response.id = document["_id"].AsObjectId;
          response.success = r.Ok;
          response.message = r.ErrorMessage;
          responses.Add(response);
        }
      }
      catch (Exception e)
      {
        var message = e.ToString();
        foreach (var d in documents)
        {
          var response = new cms_save_response();
          response.success = false;
          response.message = message;
          responses.Add(response);
        }
        if (cms_configuration.debug)
        {
          throw;
        }
      }

      return responses;
    }

    public cms_update_response update(cms_update_parameter parameter)
    {
      return update(new List<cms_update_parameter> { parameter }).Single();
    }

    public IEnumerable<cms_update_response> update(IEnumerable<cms_update_parameter> parameters)
    {
      var responses = new List<cms_update_response>();

      foreach(var p in parameters) {
        var response = new cms_update_response(p);
        responses.Add(response);

        try
        {
          var query = Query.EQ("_id", p.id);
          UpdateBuilder update;
          if (p.language == null)
          {
            update = Update.Set(p.field, p.value);
          }
          else
          {
            update = Update.Set(p.field + "." + p.language, p.value);
          }
          var collection = _db.GetCollection(p.collection);
          var result = collection.Update(query, update);
          response.success = result.Ok;
          response.message = result.ErrorMessage;
        }
        catch (Exception e)
        {
          response.message = e.ToString();
          if (cms_configuration.debug)
          {
            throw;
          }
        }
      }

      return responses;
    }

    public cms_update_response revise(cms_update_parameter parameter)
    {
      return revise(new List<cms_update_parameter> { parameter }).Single();
    }

    public IEnumerable<cms_update_response> revise(IEnumerable<cms_update_parameter> parameters)
    {
      var responses = new List<cms_update_response>();

      foreach (var p in parameters)
      {
        var response = new cms_update_response(p);
        responses.Add(response);

        try
        {
          var query = Query.EQ("_id", p.id);
          UpdateBuilder update;
          if (p.language == null)
          {
            update = Update.Push(p.field, new BsonDocument
            { 
              { "Date", DateTime.Now },
              { "Value", p.value }
            });
          }
          else
          {
            update = Update.Push(p.field + "." + p.language, new BsonDocument
            { 
              { "Date", DateTime.Now },
              { "Value", p.value }
            });
          }
          var collection = _db.GetCollection(p.collection);
          var result = collection.Update(query, update);
          response.success = result.Ok;
          response.message = result.ErrorMessage;
        }
        catch (Exception e)
        {
          response.message = e.ToString();
          if (cms_configuration.debug)
          {
            throw;
          }
        }
      }

      return responses;
    }

    public BsonDocument getCurrent(string collectionName, ObjectId id)
    {
      return getCurrent(collectionName, id, cms_configuration.language);
    }

    public IEnumerable<BsonDocument> getCurrent(string collectionName, IEnumerable<ObjectId> ids)
    {
      return getCurrent(collectionName, ids, cms_configuration.language);
    }

    public BsonDocument getCurrent(string collectionName, ObjectId id, string language)
    {
      return getCurrent(collectionName, new List<ObjectId> { id }).Single();
    }

    public IEnumerable<BsonDocument> getCurrent(string collectionName, 
      IEnumerable<ObjectId> ids, string language)
    {
      IEnumerable<BsonDocument> documents = new List<BsonDocument>();

      try
      {
        var query = Query.In("_id", ids.Select(id => new BsonObjectId(id)));
        var collection = _db.GetCollection(collectionName);
        documents = collection.Find(query).AsEnumerable<BsonDocument>();
      }
      catch (Exception e)
      {
        // TODO: handle case.
        //var message = e.ToString();
        if (cms_configuration.debug)
        {
          throw;
        }
      }

      documents = documents.Current(language);

      return documents;
    }

    public BsonDocument getField(string collectionName, ObjectId id, string fieldName)
    {
      return getField(collectionName, id, new List<string> { fieldName }).Single();
    }

    public IEnumerable<BsonDocument> getField(string collectionName, 
      ObjectId id, IEnumerable<string> fieldNames)
    {
      return getField(collectionName, new List<ObjectId> { id }, fieldNames);
    }

    public IEnumerable<BsonDocument> getField(string collectionName, 
      IEnumerable<ObjectId> ids, IEnumerable<string> fieldNames)
    {
      IEnumerable<BsonDocument> documents = new List<BsonDocument>();

      try
      {
        var query = Query.In("_id", ids.Select(id => new BsonObjectId(id)));
        var collection = _db.GetCollection(collectionName);
        documents = collection.Find(query)
          .SetFields(fieldNames.ToArray())
          .AsEnumerable<BsonDocument>();
      }
      catch (Exception e)
      {
        // TODO: handle case.
        //var message = e.ToString();
        if (cms_configuration.debug)
        {
          throw;
        }
      }

      return documents;
    }
  }
}