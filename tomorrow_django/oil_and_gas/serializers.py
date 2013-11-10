__author__ = 'lucas.fievet'

from rest_framework import serializers

from .models import (FieldProduction, Field, Country, StretchedExponential)

import logging
logger = logging.getLogger("UsLoader")


class StretchedExponentialSerializer(serializers.ModelSerializer):
    class Meta:
        model = StretchedExponential
        fields = ('date_begin', 'date_end', 'x_min', 'length', 'A', 'tau', 'beta',
                  'r_squared', 'sum_error', 'field')


class FieldFullSerializer(serializers.ModelSerializer):
    fits = StretchedExponentialSerializer(source="max_fits", many=True)

    class Meta:
        model = Field
        fields = ('id', 'name', 'country', 'discovery', 'shut_down', 'total_production_oil',
                  'current_production_oil', 'active', 'stable', 'stable_since',
                  'production_oil', 'x_min', 'A', 'tau', 'beta', 'fits')


class FieldMinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Field
        fields = ('id', 'name', 'country', 'discovery', 'shut_down', 'total_production_oil',
                  'current_production_oil', 'active', 'stable', 'stable_since',
                  'x_min', 'A', 'tau', 'beta')


class CountrySerializer(serializers.ModelSerializer):
    fits = StretchedExponentialSerializer(source="max_fits", many=True)

    class Meta:
        model = Country
        fields = ('id', 'name', 'discovery', 'shut_down', 'total_production_oil',
                  'current_production_oil', 'active', 'stable', 'stable_since',
                  'production_oil', 'x_min', 'A', 'tau', 'beta', 'fits')
