using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.Mvc;

using MongoDB.Bson;
using MongoDB.Driver;

using mvc_mongo.Models;

namespace mvc_mongo.Controllers
{
  public class CmsController : Controller
  {
    public ActionResult Index()
    {
      return View("../Tests/CmsTests");
    }

    public class cms_save_parameter
    {
      public string collectionName { get; set; }
      public BsonDocument document { get; set; }
    }

    [HttpPost]
    public JsonResult Save(cms_save_parameter parameter)
    {
      var connectionString = "mongodb://localhost";
      var client = new MongoClient(connectionString);
      var server = client.GetServer();
      var database = server.GetDatabase("test");
      var cms_handler = new cms_handler(database);
      var response = cms_handler.save(parameter.collectionName, parameter.document);
      var jsonResult = new JsonResult();
      jsonResult.Data = response.ToJson();
      return jsonResult;
    }

    [HttpPost]
    public ActionResult Create(FormCollection collection)
    {
      try
      {
        // TODO: Add insert logic here

        return RedirectToAction("Index");
      }
      catch
      {
        return View();
      }
    }

    //
    // GET: /Cms/Edit/5

    public ActionResult Edit(int id)
    {
      return View();
    }

    //
    // POST: /Cms/Edit/5

    [HttpPost]
    public ActionResult Edit(int id, FormCollection collection)
    {
      try
      {
        // TODO: Add update logic here

        return RedirectToAction("Index");
      }
      catch
      {
        return View();
      }
    }

    //
    // GET: /Cms/Delete/5

    public ActionResult Delete(int id)
    {
      return View();
    }

    //
    // POST: /Cms/Delete/5

    [HttpPost]
    public ActionResult Delete(int id, FormCollection collection)
    {
      try
      {
        // TODO: Add delete logic here

        return RedirectToAction("Index");
      }
      catch
      {
        return View();
      }
    }
  }
}
