# -*- coding: utf-8 -*-
from dj.notesgroup import models, model_serializers

from django.conf import settings
from django.db.transaction import commit_on_success

from rest_framework import generics, status
from rest_framework.response import Response

import re
import sys



def print_request(request):
    if settings.DEBUG:
        print >> sys.stderr, request.META['PATH_INFO'], 'QUERY_PARAMS:', \
            request.QUERY_PARAMS.dict(), 'DATA:', request.DATA


class BaseListView(generics.ListCreateAPIView, models.SSBase):
    paginate_by_param = 'count'

    def get(self, request, *args, **kwargs):
        print_request(request)
        return super(BaseListView, self).get(request, *args, **kwargs)

    @commit_on_success
    def post(self, request, *args, **kwargs):
        print_request(request)
        return super(BaseListView, self).post(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super(BaseListView, self).get_queryset()
        # Order_by
        for k, v in self.request.QUERY_PARAMS.items():
            test = re.match('sorting\[([\.\w]+)\]', k)
            if test:
                sort_field = test.group(1)
                sort_field = sort_field.replace('.', '__')
                if self.request.QUERY_PARAMS[k] == 'desc':
                    sort_field = '-' + sort_field
                queryset = queryset.order_by(sort_field)
        # Filter
        for k, v in self.request.QUERY_PARAMS.items():
            test = re.match('filter\[([\.\w]+)\]', k)
            if test:
                filter_field = test.group(1)
                filter_field = filter_field.replace('.', '__')
                filter_q = self.request.QUERY_PARAMS[k]
                queryset = queryset.filter(**{filter_field: filter_q})
        return queryset

    def filter_query(self, queryset, name):
        value = self.request.QUERY_PARAMS.get(name)
        if value is not None:
            queryset = queryset.filter(**{name: value})
        return queryset




class BaseElementView(generics.RetrieveUpdateDestroyAPIView, models.SSBase):

    def get(self, request, *args, **kwargs):
        print_request(request)
        return super(BaseElementView, self).get(request, *args, **kwargs)

    @commit_on_success
    def put(self, request, *args, **kwargs):
        print_request(request)
        return super(BaseElementView, self).put(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        print_request(request)
        return super(BaseElementView, self).patch(request, *args, **kwargs)

    @commit_on_success
    def destroy(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.statut = -1
        obj.save()
        return Response(status=status.HTTP_204_NO_CONTENT)



class DemandeList(BaseListView):
    model = models.Demande
    serializer_class = model_serializers.DemandeListSerializer


    def pre_save(self, obj):
        super(DemandeList, self).pre_save(obj)

    def get_queryset(self):
        queryset = super(DemandeList, self).get_queryset().filter(
            famille__statut__gte=0)
        return queryset


class DemandeElement(BaseElementView):
    model = models.Demande
    serializer_class = model_serializers.DemandeSerializer


    def update(self, request, *args, **kwargs):
        ret = super(DemandeElement, self).update(request, *args, **kwargs)
        return ret

    def post_save(self, obj, created=False):
        # send mail
        pass
