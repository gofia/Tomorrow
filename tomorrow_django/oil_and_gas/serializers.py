__author__ = 'lucas.fievet'

from rest_framework.relations import HyperlinkedRelatedField, HyperlinkedIdentityField
from rest_framework import serializers

from .models import (FieldProduction)

import logging
logger = logging.getLogger("UsLoader")


class FieldProductionSerializer(serializers.ModelSerializer):
    production = serializers.IntegerField(source='production', read_only=True)

    class Meta:
        model = FieldProduction
        fields = ('date', 'production_oil')


class FieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = FieldProduction
        fields = ('name',)
