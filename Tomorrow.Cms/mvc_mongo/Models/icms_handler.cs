using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

using MongoDB.Bson;

namespace mvc_mongo.Models
{
  interface icms_handler
  {
    cms_save_response save(string collectionName, BsonDocument document);
    IEnumerable<cms_save_response> save(string collectionName, IEnumerable<BsonDocument> documents);
    
    cms_update_response update(cms_update_parameter parameter);
    IEnumerable<cms_update_response> update(IEnumerable<cms_update_parameter> parameters);
    
    cms_update_response revise(cms_update_parameter parameter);
    IEnumerable<cms_update_response> revise(IEnumerable<cms_update_parameter> parameters);
    
    BsonDocument getCurrent(string collectionName, ObjectId id);
    IEnumerable<BsonDocument> getCurrent(string collectionName, IEnumerable<ObjectId> ids);
    BsonDocument getCurrent(string collectionName, ObjectId id, string language);
    IEnumerable<BsonDocument> getCurrent(string collectionName, IEnumerable<ObjectId> ids, string language);
    
    BsonDocument getField(string collectionName, ObjectId id, string fieldName);
    IEnumerable<BsonDocument> getField(string collectionName, ObjectId id, IEnumerable<string> fieldNames);
    IEnumerable<BsonDocument> getField(string collectionName, IEnumerable<ObjectId> ids, IEnumerable<string> fieldNames);
    //cms_response add(cms_parameter parameter);
    //IEnumerable<cms_response> add(IEnumerable<cms_parameter> parameters);
  }
}
