from django.db import models

import logging

logger = logging.getLogger("OilAndGas")

class Production(models.Model):
    logger.info("Created production.")
    name = models.CharField(max_length=50, default="")
    date = models.DateField()
    # In BBL (barrels)
    production_oil = models.PositiveIntegerField(default=0)
    # In MCF (million cubic feet)
    production_gas = models.PositiveIntegerField(null=True, default=None)
    production_water = models.PositiveIntegerField(null=True, default=None)

    @property
    def production(self):
        return self.production_oil + (self.production_gas * 1000 / 5800)

    def __str__(self):
        return self.name + " ; " + self.date.__str__() + " ; "

    class Meta:
        abstract = True
        unique_together = (("name", "date"),)


class CountryProduction(Production):
    logger.info("Created country production.")

    def __str__(self):
        return self.name + " ; " + self.date.__str__() + " ; "


class FieldProduction(Production):
    logger.info("Created field production.")
    country = models.CharField(max_length=50, default="")
    depth = models.PositiveIntegerField(null=True, default=None)

    def __str__(self):
        return self.name + " ; " + self.country + " ; " + self.date.__str__() + " ; "


class WellProduction(Production):
    logger.info("Created well production.")
    field = models.CharField(max_length=50, default="")
    country = models.CharField(max_length=50, default="")
    depth = models.PositiveIntegerField(null=True, default=None)

    def __str__(self):
        return self.name + " ; " + self.country + " ; " + self.date.__str__() + " ; "


class Field(models.Model):
    name = models.CharField(max_length=50, default="", unique=True)
    country = models.CharField(max_length=50, default="", unique=True)
    production_oil = models.TextField(default="")
    production_gas = models.TextField(default="")
    production = models.TextField(default="")
    production_oil_smooth = models.TextField(default="")
    production_gas_smooth = models.TextField(default="")
    production_smooth = models.TextField(default="")
