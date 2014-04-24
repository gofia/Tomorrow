#
# Project: Tomorrow
#
# 07 February 2014
#
# Copyright 2014 by Lucas Fievet
# Salerstrasse 19, 8050 Zuerich
# All rights reserved.
#
# This software is the confidential and proprietary information
# of Lucas Fievet. ("Confidential Information"). You
# shall not disclose such Confidential Information and shall
# use it only in accordance with the terms of the license
# agreement you entered into with Lucas Fievet.
#

from rest_framework import serializers

from .models import Field, Country, StretchedExponential


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
                  'production_oil', 'x_min', 'A', 'tau', 'beta', 'fits', 'error_avg', 'error_std')


class FieldMinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Field
        fields = ('id', 'name', 'country', 'discovery', 'shut_down', 'total_production_oil',
                  'current_production_oil', 'active', 'stable', 'stable_since',
                  'x_min', 'A', 'tau', 'beta', 'error_avg', 'error_std')


class CountrySerializer(serializers.ModelSerializer):
    fits = StretchedExponentialSerializer(source="max_fits", many=True)

    class Meta:
        model = Country
        fields = ('id', 'name', 'discovery', 'shut_down', 'total_production_oil',
                  'current_production_oil', 'active', 'stable', 'stable_since',
                  'production_oil', 'x_min', 'A', 'tau', 'beta', 'fits', 'error_avg',
                  'error_std', 'forecasts')
