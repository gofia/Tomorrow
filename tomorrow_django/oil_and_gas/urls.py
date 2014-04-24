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

from django.conf.urls import patterns, url

from . import views

oil_and_gas_urlpatterns = patterns(
    '',
    url(r'^countries',
        views.CountryList.as_view(),
        name='country-list'),
    url(r'^fields/status',
        views.FieldStatus.as_view(),
        name='field-status'),
    url(r'^fields/process/status',
        views.FieldProcessingStatus.as_view(),
        name='field-process-status'),
    url(r'^fields/process',
        views.FieldProcessing.as_view(),
        name='field-process'),
    url(r'^fields/(?P<country>[\w-]*)',
        views.FieldList.as_view(),
        name='field-list'),
    url(r'^productions/(?P<pk>[\d]*)',
        views.FieldDetails.as_view(),
        name='production-list'),
)