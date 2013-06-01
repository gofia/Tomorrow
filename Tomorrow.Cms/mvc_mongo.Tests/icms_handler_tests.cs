using System;
using Microsoft.VisualStudio.TestTools.UnitTesting;

using MongoDB.Bson;
using MongoDB.Driver;
using MongoDB.Driver.Builders;

using mvc_mongo.Models;

namespace mvc_mongo.Tests
{
  [TestClass]
  public class icms_handler_tests
  {
    [TestMethod]
    public void TestGetCurrent()
    {
      DbTest((MongoDatabase database) =>
      {
        var cms_handler = new cms_handler(database);
        var _id = mocks.BsonDocumentMock["_id"].AsObjectId;
        var actual = cms_handler.getCurrent("entities", _id);
        var expected = mocks.BsonDocumentMock.Current();
        Assert.AreEqual(expected, actual);
      });
    }

    [TestMethod]
    public void TestGetField()
    {
      DbTest((MongoDatabase database) =>
      {
        var cms_handler = new cms_handler(database);
        var _id = mocks.BsonDocumentMock["_id"].AsObjectId;
        var actual = cms_handler.getField("entities", _id, "LocalizedHistorized");
        actual = actual["LocalizedHistorized"].AsBsonDocument;
        var expected = mocks.BsonDocumentMock["LocalizedHistorized"];
        Assert.AreEqual(expected, actual);
      });
    }

    [TestMethod]
    public void TestUpdate()
    {
      DbTest((MongoDatabase database) =>
      {
        // Update object
        var cms_handler = new cms_handler(database);
        var _id = mocks.BsonDocumentMock["_id"].AsObjectId;
        var cms_parameter = new cms_update_parameter
        {
          id = _id,
          collection = "entities",
          field = "Simple",
          value = new BsonString("New value.")
        };
        var cms_response = cms_handler.update(cms_parameter);

        // Check that the update was successful
        Assert.IsTrue(cms_response.success);

        // Check that reduced entity has the expected value
        var actual = cms_handler.getCurrent("entities", _id);
        actual.OrderFields();
        var expected = mocks.BsonDocumentMock.DeepClone().AsBsonDocument;
        expected = expected.Current().AsBsonDocument;
        expected["Simple"] = new BsonString("New value.");
        expected.OrderFields();
        Assert.AreEqual(expected, actual);
      });
    }

    [TestMethod]
    public void TestLocalizedUpdate()
    {
      DbTest((MongoDatabase database) =>
      {
        // Update object
        var cms_handler = new cms_handler(database);
        var _id = mocks.BsonDocumentMock["_id"].AsObjectId;
        var cms_parameter = new cms_update_parameter
        {
          id = _id,
          collection = "entities",
          field = "Motivation",
          language = "DE",
          value = new BsonString("Neue Deutsche Motivation.")
        };
        var cms_response = cms_handler.update(cms_parameter);

        // Check that the update was successful
        Assert.IsTrue(cms_response.success);

        // Check that reduced entity has the expected value
        var actual = cms_handler.getCurrent("entities", _id, "DE");
        actual.OrderFields();
        var expected = mocks.BsonDocumentMock.DeepClone().AsBsonDocument;
        expected = expected.Current("DE").AsBsonDocument;
        expected["Motivation"] = new BsonString("Neue Deutsche Motivation.");
        expected.OrderFields();
        Assert.AreEqual(expected, actual);
      });
    }

    [TestMethod]
    public void TestRevision()
    {
      DbTest((MongoDatabase database) =>
      {
        // Update object
        var cms_handler = new cms_handler(database);
        var _id = mocks.BsonDocumentMock["_id"].AsObjectId;
        var cms_parameter = new cms_update_parameter
        {
          id = _id,
          collection = "entities",
          field = "Description",
          value = new BsonString("It is me, Lucas!")
        };
        var cms_response = cms_handler.revise(cms_parameter);

        // Check that the update was successful
        Assert.IsTrue(cms_response.success);

        // Check that reduced entity has the expected value
        var actual = cms_handler.getCurrent("entities", _id);
        actual.OrderFields();
        var expected = mocks.BsonDocumentMock.DeepClone().AsBsonDocument;
        expected = expected.Current().AsBsonDocument;
        expected["Description"] = new BsonString("It is me, Lucas!");
        expected.OrderFields();
        Assert.AreEqual(expected, actual);
      });
    }

    [TestMethod]
    public void TestLocalizedRevision()
    {
      DbTest((MongoDatabase database) =>
      {
        // Update object
        var cms_handler = new cms_handler(database);
        var _id = mocks.BsonDocumentMock["_id"].AsObjectId;
        var cms_parameter = new cms_update_parameter
        {
          id = _id,
          collection = "entities",
          field = "Biography",
          language = "DE",
          value = new BsonString("Eine neue Biography!")
        };
        var cms_response = cms_handler.revise(cms_parameter);

        // Check that the update was successful
        Assert.IsTrue(cms_response.success);

        // Check that reduced entity has the expected value
        var actual = cms_handler.getCurrent("entities", _id, "DE");
        actual.OrderFields();
        var expected = mocks.BsonDocumentMock.DeepClone().AsBsonDocument;
        expected = expected.Current().AsBsonDocument;
        expected["Biography"] = new BsonString("Eine neue Biography!");
        expected.OrderFields();
        Assert.AreEqual(expected, actual);
      });
    }

    private void DbTest(Action<MongoDatabase> action)
    {
      var connectionString = "mongodb://localhost";
      var client = new MongoClient(connectionString);
      var server = client.GetServer();
      var database = server.GetDatabase("test");
      var collection = database.GetCollection("entities");
      collection.RemoveAll();
      collection.Insert(mocks.BsonDocumentMock);
      action(database);
    }
  }
}
