using System;

using NUnit.Framework;

using MongoDB.Bson;
using MongoDB.Driver;
using mvc_mongo.Models;

namespace mvc_mongo.Tests
{
  [TestFixture]
  public class ICmsHandlerTests
  {
    [Test]
    public void TestGetCurrent()
    {
      DbTest(database =>
      {
        var cmsHandler = new cms_handler(database);
        var id = Mocks.BsonDocumentMock["_id"].AsObjectId;
        var actual = cmsHandler.getCurrent("entities", id);
        var expected = Mocks.BsonDocumentMock.Current();
        Assert.AreEqual(expected, actual);
      });
    }

    [Test]
    public void TestGetField()
    {
      DbTest(database =>
      {
        var cmsHandler = new cms_handler(database);
        var id = Mocks.BsonDocumentMock["_id"].AsObjectId;
        var actual = cmsHandler.getField("entities", id, "LocalizedHistorized");
        actual = actual["LocalizedHistorized"].AsBsonDocument;
        var expected = Mocks.BsonDocumentMock["LocalizedHistorized"];
        Assert.AreEqual(expected, actual);
      });
    }

    [Test]
    public void TestUpdate()
    {
      DbTest(database =>
      {
        // Update object
        var cmsHandler = new cms_handler(database);
        var id = Mocks.BsonDocumentMock["_id"].AsObjectId;
        var cmsParameter = new cms_update_parameter
        {
          id = id,
          collection = "entities",
          field = "Simple",
          value = new BsonString("New value.")
        };
        var cmsResponse = cmsHandler.update(cmsParameter);

        // Check that the update was successful
        Assert.IsTrue(cmsResponse.success);

        // Check that reduced entity has the expected value
        var actual = cmsHandler.getCurrent("entities", id);
        actual.OrderFields();
        var expected = Mocks.BsonDocumentMock.DeepClone().AsBsonDocument;
        expected = expected.Current().AsBsonDocument;
        expected["Simple"] = new BsonString("New value.");
        expected.OrderFields();
        Assert.AreEqual(expected, actual);
      });
    }

    [Test]
    public void TestLocalizedUpdate()
    {
      DbTest(database =>
      {
        // Update object
        var cmsHandler = new cms_handler(database);
        var id = Mocks.BsonDocumentMock["_id"].AsObjectId;
        var cmsParameter = new cms_update_parameter
        {
          id = id,
          collection = "entities",
          field = "Motivation",
          language = "DE",
          value = new BsonString("Neue Deutsche Motivation.")
        };
        var cmsResponse = cmsHandler.update(cmsParameter);

        // Check that the update was successful
        Assert.IsTrue(cmsResponse.success);

        // Check that reduced entity has the expected value
        var actual = cmsHandler.getCurrent("entities", id, "DE");
        actual.OrderFields();
        var expected = Mocks.BsonDocumentMock.DeepClone().AsBsonDocument;
        expected = expected.Current("DE").AsBsonDocument;
        expected["Motivation"] = new BsonString("Neue Deutsche Motivation.");
        expected.OrderFields();
        Assert.AreEqual(expected, actual);
      });
    }

    [Test]
    public void TestRevision()
    {
      DbTest(database =>
      {
        // Update object
        var cmsHandler = new cms_handler(database);
        var id = Mocks.BsonDocumentMock["_id"].AsObjectId;
        var cmsParameter = new cms_update_parameter
        {
          id = id,
          collection = "entities",
          field = "Description",
          value = new BsonString("It is me, Lucas!")
        };
        var cmsResponse = cmsHandler.revise(cmsParameter);

        // Check that the update was successful
        Assert.IsTrue(cmsResponse.success);

        // Check that reduced entity has the expected value
        var actual = cmsHandler.getCurrent("entities", id);
        actual.OrderFields();
        var expected = Mocks.BsonDocumentMock.DeepClone().AsBsonDocument;
        expected = expected.Current().AsBsonDocument;
        expected["Description"] = new BsonString("It is me, Lucas!");
        expected.OrderFields();
        Assert.AreEqual(expected, actual);
      });
    }

    [Test]
    public void TestLocalizedRevision()
    {
      DbTest(database =>
      {
        // Update object
        var cmsHandler = new cms_handler(database);
        var id = Mocks.BsonDocumentMock["_id"].AsObjectId;
        var cmsParameter = new cms_update_parameter
        {
          id = id,
          collection = "entities",
          field = "Biography",
          language = "DE",
          value = new BsonString("Eine neue Biography!")
        };
        var cmsResponse = cmsHandler.revise(cmsParameter);

        // Check that the update was successful
        Assert.IsTrue(cmsResponse.success);

        // Check that reduced entity has the expected value
        var actual = cmsHandler.getCurrent("entities", id, "DE");
        actual.OrderFields();
        var expected = Mocks.BsonDocumentMock.DeepClone().AsBsonDocument;
        expected = expected.Current().AsBsonDocument;
        expected["Biography"] = new BsonString("Eine neue Biography!");
        expected.OrderFields();
        Assert.AreEqual(expected, actual);
      });
    }

    private void DbTest(Action<MongoDatabase> action)
    {
      const string connectionString = "mongodb://localhost";
      var client = new MongoClient(connectionString);
      var server = client.GetServer();
      var database = server.GetDatabase("test");
      var collection = database.GetCollection("entities");
      collection.RemoveAll();
      collection.Insert(Mocks.BsonDocumentMock);
      action(database);
    }
  }
}
