# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.db.transaction import commit_on_success
from django.http import Http404

from rest_framework import generics, status
from rest_framework.response import Response

from dj.notesgroup import model_serializers
from dj.notesgroup.models import Note

import re
import sys


from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

class NGView(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def get_note_with_perms(self, pk):
        note = Note.objects.get(pk=pk)
        if not self.request.user.get_profile().can_view(note):
            raise PermissionDenied()
        return note



def print_request(request):
    if settings.DEBUG:
        print >> sys.stderr, request.META['PATH_INFO'], 'QUERY_PARAMS:', \
            request.QUERY_PARAMS.dict(), 'DATA:', request.DATA


class BaseListView(NGView, generics.ListCreateAPIView):
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




class BaseElementView(NGView, generics.RetrieveUpdateDestroyAPIView):

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



class SubTree(BaseListView):
    model = Note
    serializer_class = model_serializers.TreeListSerializer


    def pre_save(self, obj):
        super(NoteList, self).pre_save(obj)

    def get_queryset(self):
        note = self.kwargs.get('pk')
        if note is None:
            return self.request.user.get_profile().root_notes()
        note = self.get_note_with_perms(note)
        return Note.objects.filter(statut=0, parent=note, nom__isnull=False,
                                   type_note__in=(1, 2, 3)
                               ).exclude(uid=0).exclude(etat_note=4).exclude(
                                   etat_note=3).order_by('nom')


class NoteList(BaseListView):
    model = Note
    serializer_class = model_serializers.NoteListSerializer


    def pre_save(self, obj):
        super(NoteList, self).pre_save(obj)

    def get_queryset(self):
        queryset = super(NoteList, self).get_queryset().filter(
            statut=0)
        return queryset


class NoteElement(BaseElementView):
    model = Note
    serializer_class = model_serializers.NoteSerializer

    def get_queryset(self):
        note = super(NoteElement, self).get_queryset()
        if not self.request.user.get_profile().can_view(note):
            raise PermissionDenied()
        return note


    def update(self, request, *args, **kwargs):
        ret = super(NoteElement, self).update(request, *args, **kwargs)
        return ret

    def post_save(self, obj, created=False):
        # send mail
        pass
