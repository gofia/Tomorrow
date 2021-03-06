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

from datetime import date

from celery.result import AsyncResult
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib.staticfiles.views import serve

from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework import permissions, views, decorators, status
from rest_framework.reverse import reverse
from rest_framework.response import Response

from .models import (Field, Country)
from . import tasks
from .serializers import (FieldFullSerializer, FieldMinSerializer, CountrySerializer)

import logging
logger = logging.getLogger("rh")


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
            return Field.objects.filter(
                country=self.kwargs['country'],
                current_production_oil__gt=0,
                discovery__lt=date(2015, 1, 1)
            ).order_by("name").all()
        else:
            return Field.objects.all().order_by("name")


class FieldDetails(AuthenticatedView, LoggedViewMixin, RetrieveAPIView):
    model = Field
    serializer_class = FieldFullSerializer
    view_name = "field production list"


class FieldStatus(AuthenticatedView, LoggedViewMixin, views.APIView):
    model = Field
    view_name = "change stable"

    def post(self, request, format=None):
        try:
            field_id = request.DATA['id']
            field = Field.objects.get(id=field_id)
            field.stable = request.DATA['stable']
            field.save()
            return Response("", status=status.HTTP_200_OK)
        except Exception as e:
            logger("{0}".format(e))
            return Response("", status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class FieldProcessing(AuthenticatedView, LoggedViewMixin, views.APIView):
    model = Field
    view_name = "process field"

    def post(self, request, *args, **kwargs):
        try:
            field_id = request.DATA.get('field_id', None)

            if field_id is None:
                raise Exception("No field id provided")

            field = Field.objects.get(id=field_id)
            options = {
                'name': field.name,
                'start_year': request.DATA.get('start_year', 0),
                'start_month': request.DATA.get('start_month', 0),
            }
            job = tasks.process_field.delay(options)
            return Response({'job_id': job.id}, status=status.HTTP_200_OK)
        except Exception as e:
            logger("{0}".format(e))
            return Response("{0}".format(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class FieldProcessingStatus(AuthenticatedView, LoggedViewMixin, views.APIView):
    model = Field
    view_name = "field processing status"

    def post(self, request, *args, **kwargs):
        try:
            job_id = request.DATA['job_id']
            job = AsyncResult(job_id)
            data = job.result or job.state
            return Response({'status': data}, status=status.HTTP_200_OK)
        except Exception as e:
            logger("{0}".format(e))
            return Response("{0}".format(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@login_required
def oil_and_gas_base(request):
    if settings.DEBUG:
        return serve(request, '/views/production.html')
    else:
        return serve(request, '/views/production.html')
