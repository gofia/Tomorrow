__author__ = 'lucas.fievet'

from rest_framework import serializers

from .models import (FieldProduction, Field)

import logging
logger = logging.getLogger("UsLoader")


class FieldProductionSerializer(serializers.ModelSerializer):
    # production = serializers.IntegerField(source='production', read_only=True)
    # production_oil = serializers.Field(source='production_oil_json', read_only=True, many=True)

    class Meta:
        model = Field
        fields = ('name', 'production_oil', 'x_min', 'A', 'tau', 'beta')


class FieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = FieldProduction
        fields = ('name',)
