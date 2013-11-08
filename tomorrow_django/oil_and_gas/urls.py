__author__ = 'lucas.fievet'

from django.conf.urls import patterns, url

from . import views

oil_and_gas_urlpatterns = patterns(
    '',
    url(r'^countries/',
        views.CountryList.as_view(),
        name='country-list'),
    url(r'^fields/(?P<country>[\w-]*)',
        views.FieldList.as_view(),
        name='field-list'),
    url(r'^productions/(?P<name>[\W|\w-]*)/$$',
        views.FieldProductionList.as_view(),
        name='production-list'),
)