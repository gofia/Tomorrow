using NUnit.Framework;

using MongoDB.Bson;
using mvc_mongo.Models;

namespace mvc_mongo.Tests
{
  [TestFixture]
  public class BsonExtensionTests
  {
    [Test]
    public void TestValueCurrent()
    {
      var value = Mocks.BsonDocumentMock["Simple"].AsBsonValue;
      var currentValue = value.Current();
      Assert.AreEqual(value, currentValue);
    }

    [Test]
    public void TestArrayCurrent()
    {
      var array = Mocks.BsonDocumentMock["Historized"].AsBsonArray;
      var currentValue = array.Current();
      Assert.AreEqual(array[0].AsBsonDocument["Value"], currentValue);
    }

    [Test]
    public void TestLocalizedCurrent()
    {
      var document = Mocks.BsonDocumentMock["Localized"].AsBsonDocument;
      var currentValue = document.Current();
      Assert.AreEqual(document["EN"], currentValue);
    }

    [Test]
    public void TestLocalizedHistorizedCurrent()
    {
      var document = Mocks.BsonDocumentMock["LocalizedHistorized"].AsBsonDocument;
      var currentValue = document.Current();
      Assert.AreEqual(document["EN"].AsBsonArray[0].AsBsonDocument["Value"], currentValue);
    }

    [Test]
    public void TestDocumentCurrent()
    {
      var value = Mocks.BsonDocumentMock;
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

    [Test]
    public void TestDocumentLocalizedCurrent()
    {
      var value = Mocks.BsonDocumentMock;
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
