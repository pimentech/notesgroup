# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.forms import ModelForm, ValidationError, CharField, RadioSelect, \
    FloatField, Textarea, TextInput, ModelChoiceField, IntegerField, \
    FileField, EmailField, Form, Select, DateField
from django.forms.widgets import RadioFieldRenderer
from django.forms.models import inlineformset_factory
from django.utils.safestring import mark_safe
from models import Note, EtatNote, Employe, Societe, User, Attachment, Timer

from django.contrib.admin.widgets import AdminFileWidget
import unicodedata

class RadioFieldRendererNoEscape(RadioFieldRenderer):

    def render(self):
        "Outputs a <ul> for this set of radio fields."
        return mark_safe(u'\n%s\n' % u'\n'.join(
            [u'%s' % w for w in self]))


class RadioSelectNoEscape(RadioSelect):
    renderer = RadioFieldRendererNoEscape


class NGModelForm(ModelForm):

    def save(self, user, commit=True):
        super(NGModelForm, self).save(commit=False)
        if self.instance.authcrea is None:
            self.instance.authcrea = user
        self.instance.authmodif = user
        super(NGModelForm, self).save(commit=commit)


class TimerForm(NGModelForm):
    #effective_date = DateField(required=False)

    class Meta:
        model = Timer
        fields = ['duration']

    def __init__(self, *args, **kwargs):
        super(TimerForm, self).__init__(*args, **kwargs)
        instance = kwargs.get("instance")
        if instance and instance.note_id:
            self.fields['duration'] = FloatField(
                widget=Select(choices=((0, ""), (0.5, "0:30"),
                                       (1.0, "1:00"), (1.5, "1:30"),
                                       (2.0, "2:00"), (2.5, "2:30"),
                                       (3.0, "3:00"), (3.5, "3:30"),
                                       (4.0, "4:00"), (4.5, "4:30"),
                                       (5.0, "5:00"), (5.5, "5:30"),
                                       (6.0, "6:00"), (6.5, "6:30"),
                                       (7.0, "7:00"), (7.5, "7:30"),
                                       (8.0, "8:00"), (9.0, "9:00"),
                                       (10.0, "10:00"), (11.0, "11:00"),
                                       (12.0, "12:00"), (14.0, "14:00"),
                                       (18.0, "18:00"), (21.0, "21:00"),
                                       (28.0, "28:00"), (35.0, "35:00")),
                              attrs={
                                  'onChange': "updateTimer(this, '%s')"
                                  % instance.note_id
                              })
            )


class NoteAddCommentForm(NGModelForm):
    description = CharField(
        widget=Textarea(attrs={'class': 'wysiwyg',
                               'style': "height:15;width:95%;"}),
        required=False)
    etat_note = ModelChoiceField(
        queryset=EtatNote.objects.all().order_by('uid'), empty_label=None)

    class Meta:
        model = Note
        fields = ['etat_note', 'description', 'demandeur_employe',
                  'responsable_employe']

    def __init__(self, context, data, prefix, instance):
        super(NoteAddCommentForm, self).__init__(
            data=data, prefix=prefix, instance=instance)
        queryset = Employe.objects.filter(
            uid__in=[0] + context.workgroup_ids()).order_by('prenom', 'nom')
        self.fields['demandeur_employe'] = ModelChoiceField(
            queryset=queryset, empty_label=None)
        self.fields['responsable_employe'] = ModelChoiceField(
            queryset=queryset, empty_label=None)


class NoteForm(NoteAddCommentForm):
    description = CharField(
        widget=Textarea(
            attrs={'class': 'wysiwyg', 'style': "height:300;width:95%;"}),
        required=False)
    resume = CharField(
        widget=TextInput(attrs={'style': "width:40em;"}), required=True)
    priorite = IntegerField(
        widget=TextInput(attrs={'style': "width:2em;"}), required=False)
    reussite = IntegerField(
        widget=TextInput(attrs={'style': "width:4em;"}), required=False)

    class Meta:
        model = Note
        fields = [
            'nom', 'type_note', 'etat_note', 'resume', 'demandeur_employe',
            'responsable_employe', 'priorite', 'reussite', 'description']


class AttachmentForm(ModelForm):
    source = FileField(widget=AdminFileWidget)

    def clean_source(self):
        name = None
        uploaded = self.cleaned_data['source']
        if uploaded and hasattr(uploaded, '_name'):
            name = unicodedata.normalize('NFKD', uploaded._name)
            name = name.encode('ascii', 'ignore')
            name = "%s-%s" % (self.instance.note.pk, name)
            uploaded._name = name
        return uploaded


AttachmentFormSet = inlineformset_factory(
    Note, Attachment, fields=('source',), form=AttachmentForm)


class SocieteForm(NGModelForm):

    class Meta:
        model = Societe
        fields = ['nom', 'email', 'tel', 'tel2', 'adresse1',
                  'adresse2', 'cp', 'ville', 'pays', 'web']


class UserFormForUser(ModelForm):
    email2 = EmailField(label=_('Confirm Email'), required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def clean(self):
        email1 = self.cleaned_data.get('email', '')
        email2 = self.cleaned_data.get('email2', '')

        if email1 != self.instance.email:
            if email2 != email1:
                raise ValidationError(_('The two email fields did not match'))
        return self.cleaned_data


class UserForm(ModelForm):
    password = CharField(
        label=_("Password"),
        help_text=_("Retenez bien le mot de passe ; apres enregistrement,"
                    " celui-ci est crypte (sha)."))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name',
                  'email', 'password', 'is_active', 'is_staff',
                  'is_superuser']

    def __init__(self, *args, **kwargs):
        self.authenticated_user = kwargs.get('authenticated_user')
        if self.authenticated_user:
            del kwargs['authenticated_user']
        return super(UserForm, self).__init__(*args, **kwargs)

    def clean_is_superuser(self):
        if self.authenticated_user and self.authenticated_user.is_superuser \
           and self.authenticated_user.id == self.instance.id:
            if not self.cleaned_data.get('is_superuser'):
                raise ValidationError(
                    'Ne coupe pas la branche sur laquelle tu es assis.')
        return self.cleaned_data['is_superuser']


class EmployeForm(NGModelForm):

    class Meta:
        model = Employe
        fields = ['tel']


class SearchForm(Form):
    limit = IntegerField(required=False,
                         initial=50,
                         widget=Select(choices=(
                             (20, 20),
                             (50, 50),
                             (100, 100),
                             (200, 200),
                             (1000, 1000))))

    page = IntegerField(required=False)
    etat_note = IntegerField(required=False,
                             widget=Select(choices=(
                                 (-1, _("open or undefined")),
                                 (-2, _("open or resolved")),
                                 (1, _("open")),
                                 (2, _("pending")),
                                 (3, _("resolved")),
                                 (4, _("canceled")),
                                 (0, _("All")))))
    path = CharField(required=False,
                     widget=Select(choices=(
                         ("partout", _("everywhere")),
                         ("ici", _("subnotes of")),
                         #("iciplus", "arborescence de")
                     )))
    chemin = IntegerField(required=False)
    demandeur = IntegerField(required=False)
    responsable = IntegerField(required=False)

    timer_actor = IntegerField(required=False)
    timer_date = DateField(required=False, widget=TextInput(attrs={'autocomplete':"off"}))
    txt = CharField(required=False)
    sel_txt = CharField(widget=Select(choices=(
        ("resume", _("Summary")),
        ("nom", _("Name")),
        ("description", _("Description")))))

    sort_on = CharField(widget=Select(choices=(
        ("datemodif", _("Modification")),
        ("datecrea", _("Age")),
        ("nom", _("Name")),
        ("ref_etat_note", _("State")),
        ("ref_type_note", _("Type")),
        ("ref_demandeur_employe", _("From")),
        ("ref_responsable_employe", _("To")),
        ("chemin", _("Path")),
        ("priorite", _("Priority")))))
    sort_order = CharField(
        required=False, initial='-',
        widget=RadioSelect(choices=(
            ('-', mark_safe(u'<li class="fa fa-arrow-down"></li>')),
            ('', mark_safe(u'<li class="fa fa-arrow-up"></li>')))))

    date_start = DateField(required=False)
    date_end = DateField(required=False)
