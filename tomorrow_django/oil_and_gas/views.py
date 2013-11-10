from contrib.auth.decorators import login_required
from django.conf import settings
from django.http import HttpResponse
from django.utils.translation import ugettext_lazy as _
from django.contrib.staticfiles.views import serve

from rest_framework.generics import ListAPIView
from rest_framework import permissions, views, decorators
from rest_framework.reverse import reverse
from rest_framework.response import Response

from .models import (FieldProduction, Field, Country)
from .serializers import (FieldFullSerializer, FieldMinSerializer, CountrySerializer)

import logging
logger = logging.getLogger("rh")


def hello_world(request):
    return HttpResponse(_("hello world"))


class AuthenticatedOrReadOnlyView(object):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class AuthenticatedView(object):
    permission_classes = (permissions.IsAuthenticated,)


class LoggedViewMixin(object):
    def dispatch(self, request, *args, **kwargs):
        response = views.APIView.dispatch(self, request, *args, **kwargs)
        if response.status_code > 399:
            log_method = logger.warning
        elif request.method == 'GET':
            log_method = logger.debug
        else:
            log_method = logger.info

        if "slug" in kwargs:
            append = " using slug key " + kwargs["slug"]
        elif "pk" in kwargs:
            append = " using primary key " + kwargs["pk"]
        else:
            append = " with no recognised key"
        log_method("User " + request.user.username +
                   " accessed API " + self.view_name + " with method " + request.method + append)
        return response


@decorators.api_view(('GET',))
@decorators.permission_classes((permissions.IsAuthenticated,))
def api_root(request, format=None):
    logger.info("User " + request.user.username + " accessed API root.")
    return Response({
        'field-list': reverse(
            'field-list',
            request=request,
            format=format,
        ),
        'production-list': reverse(
            'production-list',
            request=request,
            format=format,
            args=("00335",),
        ),
    })


class CountryList(AuthenticatedView, LoggedViewMixin, ListAPIView):
    model = Country
    serializer_class = CountrySerializer
    view_name = "country list"

    def get_queryset(self):
        return Country.objects.all().order_by("name")


class FieldList(AuthenticatedView, LoggedViewMixin, ListAPIView):
    model = Field
    serializer_class = FieldMinSerializer
    view_name = "field list"

    def get_queryset(self):
        if self.kwargs.has_key("country") and len(self.kwargs['country']) > 0:
            return Field.objects.filter(country=self.kwargs['country']).all().order_by("name")
        else:
            return Field.objects.all().order_by("name")


class FieldDetails(AuthenticatedView, LoggedViewMixin, ListAPIView):
    model = Field
    serializer_class = FieldFullSerializer
    view_name = "field production list"

    def get_queryset(self):
        return Field.objects.filter(name=self.kwargs['name'])


@login_required
def oil_and_gas_base(request):
    if settings.DEBUG:
        return serve(request, '/views/production.html')
    else:
        return serve(request, '/views/production.html')