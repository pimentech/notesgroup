# -*- coding: utf-8 -*-
from django import template
from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.db import connection
from django.db.models import Sum
from django.http import Http404, HttpResponse
from django.template.defaultfilters import date

from django_pimentech.viewsobjects import BaseView, on_method

from models import Note, Action, Employe, Societe, Timer
from utils import note_diff, send_mail

from datetime import datetime
import forms
import json

from rest_framework import serializers


class NoteSerializer(serializers.ModelSerializer):

    def get_identity(self, data):
        try:
            return data.get('uid', None)
        except AttributeError:
            return None

    class Meta:
        model = Note
        fields = ('uid', 'nom', 'path', 'statut', 'nom', 'resume',
                  'date_debut', 'date_fin', 'reussite', 'description',
                  'demandeur_employe', 'responsable_employe',
                  'montant', 'priorite', 'etat_note', 'type_note')


active_member_required = login_required = user_passes_test(
    lambda u: u.is_active, login_url='accounts/login/')
register = template.Library()


class ActiveMemberRequiredView(BaseView):
    employe = None
    authenticated_user = None
    http_static = settings.HTTP_STATIC
    path = None

    def get_note_with_perms(self, uid):
        try:
            note = Note.objects.get(uid=uid)
        except Note.DoesNotExist:
            raise Http404
        if self.employe.can_view(note):
            return note
        raise PermissionDenied()

    @on_method(login_required)
    def __call__(self, request, *args, **kwargs):
        self.path = request.path
        self.authenticated_user = request.user
        self.employe = self.authenticated_user.get_profile()
        if 'note' in kwargs:
            kwargs['note'] = self.get_note_with_perms(kwargs['note'])
        if 'timer' in kwargs:
            kwargs['timer'] = Timer.objects.get(pk=kwargs['timer'])

        return super(ActiveMemberRequiredView, self).__call__(
            request, *args, **kwargs)

    def root_notes_ids(self):
        ids = set()
        curs = connection.cursor()
        curs.execute("select ref_note from droits where ref_employe=%s",
                     (self.request.user.id,))
        for id, in curs.fetchall():
            ids.add(id)
        return ids

    def module_note_detail_list(self, note):
        return self.inclusion_tag("notesgroup/module_note_detail_list.html",
                                  {'new': False, 'note': note})

    def module_note_detail(self, note):
        return self.inclusion_tag(
            "notesgroup/module_note_view.html",
            {'note': note, 'http_static': settings.HTTP_STATIC})


ActiveMemberRequiredView.module_note_detail_list = register.inclusion_tag(
    "notesgroup/module_note_detail_list.html")(
    ActiveMemberRequiredView.module_note_detail_list)


class IndexView(ActiveMemberRequiredView):
    template = 'notesgroup/index.html'
    note_src = None
    form = None

    def fill_context(self):
        data = self.request.POST or None
        self.note_src = self.request.GET.get('note_src')
        self.form = forms.SearchForm(data)


class ActiveMemberRequiredJsonView(ActiveMemberRequiredView):
    ret = None

    def render(self):
        return self.render_json(to_pack=self.ret, content_type='application/json')


class SubTreeView(ActiveMemberRequiredView):
    template = 'notesgroup/sub_tree.html'  # arbre_jframe
    notes = None
    note = None

    def subnotes(self):
        if self.note is None:
            return self.employe.root_notes()
        else:
            return Note.objects.filter(
                statut=0,
                parent=self.note,
                nom__isnull=False,
                type_note__in=(1, 2, 3)).exclude(
                uid=0).exclude(
                etat_note=4).exclude(
                etat_note=3).order_by('nom')

    def fill_context(self):
        self.notes = self.subnotes()
        ids = [note.pk for note in self.notes]
        if ids:
            ids = str(ids)[1:-1]
            curs = connection.cursor()
            curs.execute(
                "select distinct ref_object from note where ref_object in (%s) and ref_etat_note in (0,1) and ref_type_note in (1,2,3)" % ids)
            ids_with_subtree = [id for id, in curs.fetchall()]
            curs.execute(
                "SELECT distinct ref_note FROM droits WHERE ref_note in (%s)" % ids)
            ids_with_users = [id for id, in curs.fetchall()]
            for note in self.notes:
                note.has_subtree = note.pk in ids_with_subtree
                note.has_users = note.pk in ids_with_users


class SubTreeJSON(SubTreeView):

    def fill_context(self):
        notes = [{'name': note.nom,
                  'id': str(note.pk),
                  'path': note.path} for note in self.subnotes()]
        return self.render_json(notes)


class NoteListView(ActiveMemberRequiredView):
    template = 'notesgroup/note_list.html'
    limit = 50
    notes = None
    parent_note = None
    duration = 0.0
    duration_in_days = None
    timer_duration = 0
    timer_date = None
    form = None
    human_path_dict = None

    def fill_context(self):
        data = self.request.POST or None
        self.form = forms.SearchForm(data)
        self.notes = []
        if self.form.data and self.form.is_valid():
            if self.authenticated_user.is_superuser:
                self.notes = Note.objects.exclude(uid=0)
            else:
                paths = ["note.path LIKE '" + note.path + "/%%'"
                         for note in self.employe.root_notes()]
                self.notes = Note.objects.extra(
                    where=["(%s)" % (" OR ".join(paths))])
            c = self.form.cleaned_data

            if c['timer_actor'] and c['timer_date']:
                self.notes = self.notes.filter(
                    timer__employe=c['timer_actor'],
                    timer__effective_date=c['timer_date'])
            if c['chemin'] is not None:
                self.parent_note = Note.objects.get(pk=c['chemin'])
                if c['path'] == 'ici':
                    self.notes = self.notes.filter(parent=self.parent_note)
                # elif c['path'] == 'iciplus':
                # self.notes = self.notes.filter(path__startswith=c['chemin'])
            if c['etat_note']:
                if c['etat_note'] == -1:
                    self.notes = self.notes.filter(etat_note__in=(1, 0))
                else:
                    self.notes = self.notes.filter(etat_note=c['etat_note'])
            if c['demandeur']:
                self.notes = self.notes.filter(
                    demandeur_employe=c['demandeur'])
            if c['responsable']:
                self.notes = self.notes.filter(
                    responsable_employe__in=(c['responsable'], 0))
            if c['date_start']:
                self.notes = self.notes.filter(datemodif__gte=c['date_start'])
            if c['date_end']:
                self.notes = self.notes.filter(datemodif__lte=c['date_end'])

            if c['txt']:
                if c['sel_txt'] == 'resume':
                    self.notes = self.notes.filter(resume__icontains=c['txt'])
                elif c['sel_txt'] == 'nom':
                    self.notes = self.notes.filter(nom__icontains=c['txt'])
                else:
                    self.notes = self.notes.filter(
                        description__icontains=c['txt'])
            self.notes = self.notes.order_by(
                '%s%s' % (c['sort_order'], c['sort_on']))
            paginator = Paginator(self.notes, c['limit'])

            # If page request (9999) is out of range, deliver last page of
            # results.
            try:
                self.notes = paginator.page(c['page'])
            except (EmptyPage, InvalidPage):
                self.notes = paginator.page(paginator.num_pages)

            note_name = {}
            self.timer_date = c['timer_date'] or datetime.today()
            for note in self.notes.object_list:
                try:
                    note.timer = Timer.objects.get(
                        note=note, employe=self.employe,
                        effective_date=self.timer_date)
                    self.timer_duration += note.timer.duration
                except Timer.DoesNotExist:
                    note.timer = None

                ids = note.path.split('/')[1:-1]
                for id in ids:
                    note_name[int(id)] = None
                self.duration += note.montant or 0.5

            self.duration_in_days = self.duration / 7

            ids = note_name.keys()

            if ids and c['chemin'] is not None and c['path'] == 'ici':
                self.human_path_dict = {}
                curs = connection.cursor()
                curs.execute("select uid, nom from note where uid in (%s)" %
                             str(ids)[1:-1])
                for id, nom in curs.fetchall():
                    note_name[id] = nom
                for note in self.notes.object_list:
                    ids = note.path.split('/')[1:-1]
                    human_path = []
                    for id in ids:
                        human_path.append(note_name[int(id)])
                    human_path = '/' + '/'.join(human_path)
                    note.human_path = human_path
                    self.human_path_dict[note.pk] = human_path

                self.human_path_dict = json.dumps(self.human_path_dict,
                                                  ensure_ascii=False,
                                                  cls=json.JSONEncoder)


class NoteListJsonView(ActiveMemberRequiredJsonView):

    def fill_context(self):
        super(NoteListJsonView, self).fill_context()
        serializer = NoteSerializer(self.notes, many=True)
        self.ret = serializer.data


class DetailListView(ActiveMemberRequiredView):
    template = 'notesgroup/module_note_detail_list.html'
    note = None
    events = True
    new = False

    def fill_context(self):
        # Redirection after note creation.
        self.new = 'new' in self.request.GET


class NoteDetailView(ActiveMemberRequiredView):
    template = 'notesgroup/note_detail.html'
    note = None


class NoteDetailNewWindowView(ActiveMemberRequiredView):
    template = 'notesgroup/note_detail_new_window.html'
    note = None


class EditView(ActiveMemberRequiredView):
    template = 'notesgroup/edit_form.html'
    action = 'edit'  # or 'new'
    form = None
    timer_form = None


class NoteDiffView(ActiveMemberRequiredView):
    note = None

    def fill_context(self):
        previous = Action.objects.filter(
            object=self.note).order_by('-datemodif')[0]
        return note_diff(previous, self.note)


class TimerEditView(ActiveMemberRequiredView):
    note = None
    timer = None
    form = None

    def fill_context(self):
        data = self.request.POST or None
        instance = self.timer
        if not instance:
            instance = Timer(
                employe=self.employe,
                note=self.note,
                effective_date=datetime.today()
            )
        form = forms.TimerForm(data, instance=instance)
        if data and form.is_valid():
            form.save()


class SetTimerView(ActiveMemberRequiredView):
    note = None

    def fill_context(self):
        data = self.request.POST or self.request.GET or None
        duration = float(data['duration'])

        timer, created = Timer.objects.get_or_create(
            note=self.note, employe=self.employe,
            effective_date=datetime.today())
        if timer.duration != duration:
            self.note.montant = (self.note.montant or 0) + \
                                duration - (timer.duration or 0.0)
            self.note.save()
            timer.duration = duration
            timer.save()
        return HttpResponse('OK')


class GetTimerDayView(ActiveMemberRequiredView):
    def fill_context(self):
        duration = Timer.objects.filter(employe=self.employe,
                                        effective_date=datetime.today())
        duration = duration.aggregate(work=Sum('duration'))['work']
        return HttpResponse(unicode(duration))



class NoteEditView(EditView):
    template = 'notesgroup/note_edit.html'
    FormClass = forms.NoteForm
    note = None
    attachment_formset = None
    new = None
    done_message = None

    def fill_context(self):
        data = self.request.POST or None
        instance = self.note
        if self.action == 'edit':
            self.attachment_formset = forms.AttachmentFormSet(
                data,
                self.request.FILES or None,
                instance=self.note,
                prefix='attachment')
        elif self.action == 'add_comment':
            old_description = instance.description
            instance.description = ''
        elif self.action == 'new':
            instance = Note(auteur_employe=self.employe,
                            demandeur_employe=self.employe,
                            type_note_id=4,
                            etat_note_id=1,
                            description='',
                            parent=self.note)
        else:
            raise NotImplemented
        if instance.pk:
            try:
                timer = Timer.objects.get(
                    note=instance, employe=self.employe,
                    effective_date=datetime.today())
            except Timer.DoesNotExist:
                timer = Timer(note=instance)
            self.timer_form = forms.TimerForm(instance=timer)

        self.form = self.FormClass(context=self.note, data=data,
                                   instance=instance,
                                   prefix=str(self.note.uid))
        if data:
            is_valid = True
            if self.attachment_formset:
                if self.attachment_formset.is_valid():
                    self.attachment_formset.save()
                else:
                    is_valid = False
            if self.form.is_valid():
                if self.action == 'add_comment':
                    comment = self.form.cleaned_data['description']
                    self.form.instance.description = '%s\n' \
                        '<div class="group"><h6>%s %s</h6>\n' \
                        '<p>%s</p>\n' \
                        '</div><br/>' % (old_description,
                                         self.request.user, date(
                                             datetime.now(), "r"),
                                         comment)
                self.form.save(self.authenticated_user)

                timer, created = Timer.objects.get_or_create(
                    note=self.form.instance, employe=self.employe,
                    effective_date=datetime.today())
                timer.save()
                self.context['uid'] = self.form.instance.parent_id
            else:
                is_valid = False
            if is_valid:
                self.form.instance.notify_modifs()
                self.template = 'notesgroup/module_note_detail_list.html'
                self.done_message = True
                if self.action == 'new':
                    self.new = True
                    self.note = self.form.instance
                else:
                    self.new = False


class NoteAddCommentView(NoteEditView):
    template = 'notesgroup/note_add_comment.html'
    action = 'add_comment'
    FormClass = forms.NoteAddCommentForm


class SocieteEditView(EditView):
    societe = None

    def fill_context(self):
        data = self.request.POST or None
        if self.authenticated_user.is_superuser:
            if self.action == 'edit':
                try:
                    self.societe = Societe.objects.get(uid=self.societe)
                    instance = self.societe
                except Societe.DoesNotExist:
                    raise Http404
            else:
                instance = Societe()
        elif self.action == 'edit' and str(self.societe) == str(self.employe.societe_id):
            self.societe = self.employe.societe
            instance = self.societe
        else:
            raise PermissionDenied()
        self.form = forms.SocieteForm(data=data, instance=instance)
        if data and self.form.is_valid():
            self.form.save(self.authenticated_user)


class UserEditView(EditView):
    template = 'notesgroup/user_edit.html'
    _user_edit = None
    employe_form = None
    societe = None

    def fill_context(self):
        data = self.request.POST or None
        user_form_cls = forms.UserForm
        user_form_kwargs = {'authenticated_user': self.authenticated_user}

        if self._user_edit and self.action == 'edit' \
           and self.authenticated_user.is_superuser:
            try:
                user = User.objects.get(id=self._user_edit)
                employe = user.get_profile()
            except User.DoesNotExist:
                raise Http404
        elif self.action == 'new' and self.authenticated_user.is_superuser:
            try:
                self.societe = Societe.objects.get(uid=self.societe)
            except Societe.DoesNotExist:
                raise Http404
            user = User()
            employe = Employe(societe=self.societe, type_employe_id=0)
        elif self.action == 'edit' and int(self._user_edit) == self.authenticated_user.id:
            user = User.objects.get(id=self._user_edit)
            employe = user.get_profile()
            user_form_cls = forms.UserFormForUser
            user_form_kwargs = {}
        else:
            raise PermissionDenied()
        self.form = user_form_cls(
            data=data, instance=user, prefix='user', **user_form_kwargs)
        self.employe_form = forms.EmployeForm(
            data=data, instance=employe, prefix='employe')
        if data and self.form.is_valid() and self.employe_form.is_valid():
            self.form.save()
            user = self.form.instance
            if not user.password.startswith('sha1$'):
                creator = self.request.user.get_profile()
                send_mail(None, [user], u"Welcome to NotesGroup", u"""
<h1>Welcome to NotesGroup</h1>
<p>
A NotesGroup access has been created for you by %s %s (%s).
</p>
You are invited to login to to %s with these accesses :<br />
login : %s<br />
password : %s<br />
<br />

<b>Please keep this e-mail, your password is encrypted in the application and can't be retreived.</b>
""" % (creator.prenom, creator.nom, creator.email,
                    settings.HTTP_ROOT, user.username, user.password))
                user.set_password(user.password)
                user.save()
            self.employe_form.instance.uid = user.id
            self.employe_form.instance.user = user
            self.employe_form.instance.prenom = user.first_name
            self.employe_form.instance.nom = user.last_name
            self.employe_form.instance.email = user.email
            self.employe_form.save(self.authenticated_user)
            if not user.is_active:
                employe.delete_droits()
            self.form = user_form_cls(instance=user, prefix='user')
            self.employe_form = forms.EmployeForm(
                instance=employe, prefix='employe')


class NoteUsersView(ActiveMemberRequiredView):
    template = 'notesgroup/note_users.html'
    note = None

    def fill_context(self):
        user_id = self.request.GET and self.request.GET.get('user')
        if user_id:
            action = self.request.GET['action']
            if self.authenticated_user.is_superuser:
                user = User.objects.get(pk=user_id)
                if action == 'del':
                    self.note.del_user(user_id)
                    self.note.notify(
                        self.request.user,
                        u"%s %s a été supprimé de l'arborescence à la note «%s»" % (
                            user.first_name, user.last_name, self.note)
                    )
                elif action == 'add':
                    self.note.add_user(self.authenticated_user, user_id)
                    self.note.notify(
                        self.request.user,
                        u"%s %s a été ajouté dans l'arborescence sur la note «%s»" % (
                            user.first_name, user.last_name, self.note)
                    )
            else:
                raise PermissionDenied()


class NoteMoveView(ActiveMemberRequiredView):
    note = None
    new_parent = None

    def fill_context(self):
        self.new_parent = self.get_note_with_perms(self.new_parent)
        self.note.parent = self.new_parent
        self.note.path = None  # re-set in save
        self.note.save()
        return HttpResponse("OK")


class WorkGroupView(ActiveMemberRequiredView):
    template = 'notesgroup/workgroup.html'


class FooView(ActiveMemberRequiredView):
    template = 'notesgroup/note_detail.html'
    note = None

    def fill_context(self):
        self.note = Note.objects.get(note=self.note)
        self['toto'] = 'popo'
