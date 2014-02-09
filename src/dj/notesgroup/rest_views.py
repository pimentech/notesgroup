# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import connection
from django.db.models import get_model
from django.db.transaction import commit_on_success
from django.http import Http404, HttpResponse

from rest_framework import generics, serializers, status
from rest_framework.response import Response

import datetime, re
import sys
import warnings
import types

#rm dj.notesgroup.views import ActiveMemberRequiredView


def print_request(request):
    if settings.DEBUG:
        print >> sys.stderr, request.META['PATH_INFO'], 'QUERY_PARAMS:', \
            request.QUERY_PARAMS.dict(), 'DATA:', request.DATA


class BaseListView(generics.ListCreateAPIView):
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
                queryset = queryset.filter(**{filter_field:filter_q})
        return queryset

    def filter_query(self, queryset, name):
        value = self.request.QUERY_PARAMS.get(name)
        if value is not None:
            queryset = queryset.filter(**{name:value})
        return queryset








class BaseElementView(generics.RetrieveUpdateDestroyAPIView):
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



def dictfetchall(cursor):
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]


class SSSerializer(serializers.ModelSerializer):
    def get_identity(self, data):
        try:
            return data.get('uid', None)
        except AttributeError:
            return None


class ValidSerializer(SSSerializer):
    def field_to_native(self, obj, field_name):
        """
        Override default so that the serializer can be used as a nested field
        across relationships.
        """
        if self.source == '*':
            return self.to_native(obj)
        # Get the raw field value
        try:
            source = self.source or field_name
            value = obj
            for component in source.split('.'):
                if value is None:
                    break
                value = get_component(value, component)
        except ObjectDoesNotExist:
            return None
        if is_simple_callable(getattr(value, 'all', None)):
            # la seule modif est ici :
            # s/all()/exclude(statut=-1)
            return [self.to_native(item) for item in value.exclude(statut=-1)]
        if value is None:
            return None
        if self.many is not None:
            many = self.many
        else:
            many = hasattr(value, '__iter__') and not isinstance(value, (Page, dict,
                                                                         six.text_type))
        if many:
            return [self.to_native(item) for item in value]
        return self.to_native(value)


class NoteSerializer(SSSerializer):
    class Meta:
        model = models.Personne
        fields = ('uid', 'nom', 'path', 'statut', 'nom', 'resume'
                  'date_debut', 'date_fin', 'reussite',
                  'description', 'demandeur_employe', 'responsable_employe',
                  'montant', 'priorite', 'etat_note', 'type_note')


class NoteList(BaseListView):
    model = models.Note
    serializer_class = NoteSerializer
    queryset = Note.objects.filter(statut=0)
    def get_queryset(self):
        queryset = super(DispoList, self).get_queryset()
        dispo_le = self.request.QUERY_PARAMS.get('dispo_le')
        #import ipdb;ipdb.set_trace()
        if not dispo_le:
            dispo_le = datetime.date.today()
        else:
            dispo_le = dateutil.parser.parse(dispo_le)#[1:-1])
        return queryset.filter(debut__lte=dispo_le, fin__gte=dispo_le)
