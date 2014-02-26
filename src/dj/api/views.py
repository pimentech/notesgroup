# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.db import connection
from django.db.transaction import commit_on_success
from rest_framework import generics, status
from rest_framework.response import Response

from dj.notesgroup import model_serializers
from dj.notesgroup.models import Note, Timer
from dj.notesgroup import forms

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from datetime import datetime
import re
import sys

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


class BaseCreateView(NGView, generics.CreateAPIView):
    @commit_on_success
    def post(self, request, *args, **kwargs):
        print_request(request)
        return super(BaseListView, self).post(request, *args, **kwargs)


class BaseListView(BaseCreateView, generics.ListCreateAPIView):
    paginate_by_param = 'count'

    def get(self, request, *args, **kwargs):
        print_request(request)
        return super(BaseListView, self).get(request, *args, **kwargs)

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

from django import http
from django.utils import simplejson as json

class JSONResponseMixin(object):
    def render_to_response(self, context):
        "Returns a JSON response containing 'context' as payload"
        return self.get_json_response(self.convert_context_to_json(context))

    def get_json_response(self, content, **httpresponse_kwargs):
        "Construct an `HttpResponse` object."
        return http.HttpResponse(content,
                                 content_type='application/json',
                                 **httpresponse_kwargs)

    def convert_context_to_json(self, context):
        "Convert the context dictionary into a JSON object"
        # Note: This is *EXTREMELY* naive; in reality, you'll need
        # to do much more complex handling to ensure that arbitrary
        # objects -- such as Django model instances or querysets
        # -- can be serialized as JSON.
        return json.dumps(context)

from django.views.generic.detail import BaseDetailView

class Tree(JSONResponseMixin, BaseDetailView):

    def get(self, request, *args, **kwargs):
        curs = connection.cursor()
        if request.user.is_superuser:
            root_notes = ((0, 'Notesgroup', '/'),)
        else:
            employe = request.user.get_profile()
            curs.execute(
                "SELECT note.uid,note.nom,note.path FROM droits,note WHERE"
                " droits.ref_employe=%s AND droits.ref_note=note.uid"
                " AND note.statut=0 ORDER BY note.path", (employe.pk,))
            root_notes = curs.fetchall()
        paths = []
        node_dict = {}
        tree = []
        for uid,nom,path in root_notes:
            if not paths or not path.startswith(paths[-1]):
                paths.append(path)
                node = {'uid':uid, 'nom':nom}
                node_dict[uid] = node
                tree.append(node)
        for path in paths:
            curs.execute(
                "SELECT uid,ref_object,nom FROM note WHERE path like %s"
                " AND ref_type_note in (1,2,3) AND ref_etat_note not in (3,4)"
                " AND uid!=0 AND nom is not null ORDER BY path", (path+'%',))
            for uid, parent_uid, nom in curs.fetchall():
                node = {'uid':uid,'nom':nom}
                if parent_uid in node_dict:
                    parent = node_dict[parent_uid]
                    if 'children' in parent:
                        parent['children'].append(node)
                    else:
                        parent['children'] = [ node ]
                node_dict[uid] = node
        return self.render_to_response(tree)


class NoteList(BaseListView):
    model = Note
    serializer_class = model_serializers.NoteListSerializer
    employe = None
    form = None

    def pre_save(self, obj):
        super(NoteList, self).pre_save(obj)

    def get_queryset(self):
        self.employe = self.request.user.get_profile()
        notes = []
        data = self.request.POST or self.request.GET or None
        self.form = forms.SearchForm(data)
        #self.notes = []
        if self.form.data and self.form.is_valid():
            if self.request.user.is_superuser:
                notes = Note.objects.exclude(uid=0)
            else:
                paths = ["note.path LIKE '" + note.path + "/%%'"
                         for note in self.employe.root_notes()]
                notes = Note.objects.extra(
                    where=["(%s)" % (" OR ".join(paths))])
            c = self.form.cleaned_data

            if c['timer_actor'] and c['timer_date']:
                notes = notes.filter(
                    timer__employe=c['timer_actor'],
                    timer__effective_date=c['timer_date'])
            if c['chemin'] is not None:
                self.parent_note = Note.objects.get(pk=c['chemin'])
                if c['path'] == 'ici':
                    notes = notes.filter(parent=self.parent_note)
            if c['etat_note']:
                if c['etat_note'] == -1:
                    notes = notes.filter(etat_note__in=(1, 0))
                else:
                    notes = notes.filter(etat_note=c['etat_note'])
            if c['demandeur']:
                notes = notes.filter(demandeur_employe=c['demandeur'])
            if c['responsable']:
                notes = notes.filter(responsable_employe__in=(c['responsable'], 0))
            if c['date_start']:
                notes = notes.filter(datemodif__gte=c['date_start'])
            if c['date_end']:
                notes = notes.filter(datemodif__lte=c['date_end'])
            if c['txt']:
                if c['sel_txt'] == 'resume':
                    notes = notes.filter(resume__icontains=c['txt'])
                elif c['sel_txt'] == 'nom':
                    notes = notes.filter(nom__icontains=c['txt'])
                else:
                    notes = notes.filter(description__icontains=c['txt'])
            notes = notes.order_by('%s%s' % (c['sort_order'], c['sort_on']))

        return notes


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


class TimerCreate(BaseCreateView):
    model = Timer
    serializer_class = model_serializers.TimerSerializer

    def pre_save(self, obj):
        super(TimerCreate, self).pre_save(obj)
        note = self.kwargs.get('pk')
        obj.note = self.get_note_with_perms(note)
        obj.employe = self.request.user.get_profile()
        obj.effective_date = datetime.today()


class TimerElement(BaseElementView):
    model = Timer
    serializer_class = model_serializers.TimerSerializer
