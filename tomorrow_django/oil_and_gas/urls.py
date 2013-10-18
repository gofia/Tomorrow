__author__ = 'lucas.fievet'

from django.conf.urls import patterns, url

from . import views

oil_and_gas_urlpatterns = patterns(
    '',
    url(r'^fields/',
        views.FieldList.as_view(),
        name='field-list'),
    url(r'^productions/(?P<name>[\w-]*)/$$',
        views.FieldProductionList.as_view(),
        name='production-list'),
)