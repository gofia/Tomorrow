__author__ = 'lucas.fievet'

from rest_framework import serializers

from .models import (FieldProduction, Field, StretchedExponential)

import logging
logger = logging.getLogger("UsLoader")


class StretchedExponentialSerializer(serializers.ModelSerializer):
    class Meta:
        model = StretchedExponential
        fields = ('date_begin', 'date_end', 'x_min', 'length', 'A', 'tau', 'beta', 'r_squared', 'sum_error', 'field')


class FieldProductionSerializer(serializers.ModelSerializer):
    fits = StretchedExponentialSerializer(source="max_fits", many=True)

    class Meta:
        model = Field
        fields = ('name', 'production_oil', 'x_min', 'A', 'tau', 'beta', 'fits')


class FieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = FieldProduction
        fields = ('name',)
