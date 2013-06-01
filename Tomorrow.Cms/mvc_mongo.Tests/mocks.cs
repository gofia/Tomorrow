using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

using MongoDB.Bson;

namespace mvc_mongo.Tests
{
  public static class mocks
  {
    public static BsonDocument BsonDocumentMock = new BsonDocument
    {
      { "_id", new ObjectId("51914677d185ee1584acea23") },
      { "Simple", "value" },
      { "Historized", 
        new BsonArray { 
          new BsonDocument { 
            { "Date", DateTime.Now },
            { "Value", "Value now." }
          } 
        }
      },
      { "Localized",
        new BsonDocument { 
          { "EN", "English value." },
          { "DE", "Deutscher Wert." }
        }
      },
      { "LocalizedHistorized",
        new BsonDocument { 
          { "EN",  
            new BsonArray { 
              new BsonDocument { 
                { "Date", DateTime.Now },
                { "Value", "Value now." }
              }, 
              new BsonDocument { 
                { "Date", DateTime.Now.AddDays(-1) },
                { "Value", "Previous value." }
              }
            } 
          },
          { "DE",  
            new BsonArray { 
              new BsonDocument { 
                { "Date", DateTime.Now },
                { "Value", "Deutscher Wert." }
              } 
            }
          }
        }
      }
    };
  }
}
