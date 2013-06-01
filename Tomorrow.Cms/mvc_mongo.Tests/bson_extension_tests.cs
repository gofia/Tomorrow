using System;

using Microsoft.VisualStudio.TestTools.UnitTesting;

//using NUnit.Framework;

using MongoDB.Bson;

using mvc_mongo.Models;

namespace mvc_mongo.Tests
{
  //[TestFixture]
  [TestClass]
  public class bson_extension_tests
  {
    [TestMethod]
    public void TestValueCurrent()
    {
      var value = mocks.BsonDocumentMock["Simple"].AsBsonValue;
      var currentValue = value.Current();
      Assert.AreEqual(value, currentValue);
    }

    //[Test]
    [TestMethod]
    public void TestArrayCurrent()
    {
      var array = mocks.BsonDocumentMock["Historized"].AsBsonArray;
      var currentValue = array.Current();
      Assert.AreEqual(array[0].AsBsonDocument["Value"], currentValue);
    }

    [TestMethod]
    public void TestLocalizedCurrent()
    {
      var document = mocks.BsonDocumentMock["Localized"].AsBsonDocument;
      var currentValue = document.Current();
      Assert.AreEqual(document["EN"], currentValue);
    }

    [TestMethod]
    public void TestLocalizedHistorizedCurrent()
    {
      var document = mocks.BsonDocumentMock["LocalizedHistorized"].AsBsonDocument;
      var currentValue = document.Current();
      Assert.AreEqual(document["EN"].AsBsonArray[0].AsBsonDocument["Value"], currentValue);
    }

    [TestMethod]
    public void TestDocumentCurrent()
    {
      var value = mocks.BsonDocumentMock;
      var currentValue = value.Current();

      var expected = new BsonDocument
      {
        { "_id", new ObjectId("51914677d185ee1584acea23") },
        { "Simple", "value" },
        { "Historized", "Value now." },
        { "Localized", "English value." },
        { "LocalizedHistorized", "Value now." }
      };

      Assert.AreEqual(expected, currentValue);
    }

    [TestMethod]
    public void TestDocumentLocalizedCurrent()
    {
      var value = mocks.BsonDocumentMock;
      var currentValue = value.Current("DE");

      var expected = new BsonDocument
      {
        { "_id", new ObjectId("51914677d185ee1584acea23") },
        { "Simple", "value" },
        { "Historized", "Value now." },
        { "Localized", "Deutscher Wert." },
        { "LocalizedHistorized", "Deutscher Wert." }
      };

      Assert.AreEqual(expected, currentValue);
    }
  }
}
