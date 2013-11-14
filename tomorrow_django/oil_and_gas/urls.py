__author__ = 'lucas.fievet'

from django.conf.urls import patterns, url

from . import views

oil_and_gas_urlpatterns = patterns(
    '',
    url(r'^countries',
        views.CountryList.as_view(),
        name='country-list'),
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