# -*- coding: utf-8 -*-
from django.conf import settings
from django.db.models import signals, Model, Manager, AutoField, ForeignKey, \
    CharField, IntegerField, FloatField, DateField, DateTimeField, \
    EmailField, BooleanField, FileField
from django.db import connection
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage

from entities import entities
from utils import send_mail, note_diff
import inspect

import os
import sys
import datetime
from django.utils.translation import ugettext as _


def save(instance, authenticated_user):
    if instance.authcrea is None:
        instance.authcrea = authenticated_user
    instance.authmodif = authenticated_user
    instance.save()


def _set_paths(parent):
    try:
        for note in Note.objects.filter(parent=parent):
            note.path = parent.path + '/%s' % note.uid
            note.save()
            _set_paths(note)
    except:
        pass


def set_paths():
    for note in Note.objects.filter(parent=0).exclude(uid=0):
        note.path = '/%s' % note.uid
        note.save()
        _set_paths(note)


class Object(Model):

    class Meta:
        db_table = 'object'

    uid = AutoField('ID', primary_key=True)
    authcrea = ForeignKey(User, db_column='authcrea',
                          related_name='object_authcrea', editable=False, null=True, blank=True)
    authmodif = ForeignKey(User, db_column='authmodif',
                           related_name='object_authmodif', editable=False, null=True, blank=True)
    codecrea = CharField(max_length=200, null=True, blank=True)
    codemodif = CharField(max_length=200, null=True, blank=True)
    datecrea = DateTimeField(auto_now_add=True, null=True, blank=True)
    datemodif = DateTimeField(auto_now_add=True, null=True, blank=True)
    nom = CharField(max_length=200, null=True, blank=True)
    statut = IntegerField(default=0, null=True, blank=True)


class TypeEmploye(Model):

    class Meta:
        db_table = 'type_employe'

    uid = AutoField('ID', primary_key=True)
    authcrea = ForeignKey(User, db_column='authcrea',
                          related_name='type_employe_authcrea',
                          editable=False, null=True, blank=True)
    authmodif = ForeignKey(User, db_column='authmodif',
                           related_name='type_employe_authmodif',
                           editable=False, null=True, blank=True)
    codecrea = CharField(max_length=200, null=True, blank=True)
    codemodif = CharField(max_length=200, null=True, blank=True)
    datecrea = DateTimeField(auto_now_add=True, null=True, blank=True)
    datemodif = DateTimeField(auto_now_add=True, null=True, blank=True)
    nom = CharField(max_length=200, null=True, blank=True)
    statut = IntegerField(default=0, null=True, blank=True)

    def __unicode__(self):
        return self.nom


class Personne(Model):

    class Meta:
        db_table = 'personne'

    uid = AutoField('ID', primary_key=True)
    authcrea = ForeignKey(User, db_column='authcrea',
                          related_name='personne_authcrea', editable=False,
                          null=True, blank=True)
    authmodif = ForeignKey(User, db_column='authmodif',
                           related_name='personne_authmodif', editable=False,
                           null=True, blank=True)
    codecrea = CharField(max_length=200, null=True, blank=True)
    codemodif = CharField(max_length=200, null=True, blank=True)
    datecrea = DateTimeField(auto_now_add=True, null=True, blank=True)
    datemodif = DateTimeField(auto_now_add=True, null=True, blank=True)
    nom = CharField(max_length=200, null=True, blank=True)
    statut = IntegerField(default=0, null=True, blank=True)
    adresse1 = CharField(max_length=200, null=True, blank=True)
    adresse2 = CharField(max_length=200, null=True, blank=True)
    commentaire = CharField(max_length=200, null=True, blank=True)
    cp = CharField(max_length=200, null=True, blank=True)
    email = CharField(max_length=200, null=True, blank=True, unique=True)
    euid = CharField(max_length=200, null=True, blank=True)
    fax = CharField(max_length=200, null=True, blank=True)
    pays = CharField(max_length=200, null=True, blank=True)
    tel = CharField(max_length=200, null=True, blank=True)
    tel2 = CharField(max_length=200, null=True, blank=True)
    ville = CharField(max_length=200, null=True, blank=True)
    web = CharField(max_length=200, null=True, blank=True)


class Societe(Model):

    class Meta:
        db_table = 'societe'

    uid = AutoField('ID', primary_key=True)
    statut = IntegerField(default=0, null=True, blank=True)
    authcrea = ForeignKey(User, db_column='authcrea',
                          related_name='societe_authcrea',
                          null=True, blank=True)
    authmodif = ForeignKey(User, db_column='authmodif',
                           related_name='societe_authmodif',
                           null=True, blank=True)
    codecrea = CharField(max_length=200, null=True, blank=True)
    codemodif = CharField(max_length=200, null=True, blank=True)
    datecrea = DateTimeField(auto_now_add=True, null=True, blank=True)
    datemodif = DateTimeField(auto_now_add=True, null=True, blank=True)

    nom = CharField(max_length=200, null=True, blank=True, unique=True)
    adresse1 = CharField(max_length=200, null=True, blank=True)
    adresse2 = CharField(max_length=200, null=True, blank=True)
    cp = CharField(max_length=200, null=True, blank=True)
    ville = CharField(max_length=200, null=True, blank=True)
    pays = CharField(max_length=200, null=True, blank=True)

    email = EmailField(max_length=200, null=True, blank=True)

    commentaire = CharField(max_length=200, null=True, blank=True)
    euid = CharField(max_length=200, null=True, blank=True)
    fax = CharField(max_length=200, null=True, blank=True)
    tel = CharField(max_length=200, null=True, blank=True)
    tel2 = CharField(max_length=200, null=True, blank=True)
    web = CharField(max_length=200, null=True, blank=True)
    logo = CharField(max_length=200, null=True, blank=True)
    raison = CharField(max_length=200, null=True, blank=True)
    siren = CharField(max_length=200, null=True, blank=True)
    siret = CharField(max_length=200, null=True, blank=True)
    ue_tva = CharField(max_length=200, null=True, blank=True)

    def __unicode__(self):
        return self.nom


class PersonnePhysique(Model):

    class Meta:
        db_table = 'personne_physique'

    uid = AutoField('ID', primary_key=True)
    authcrea = ForeignKey(User, db_column='authcrea',
                          related_name='personne_physique_authcrea',
                          editable=False, null=True, blank=True)
    authmodif = ForeignKey(User, db_column='authmodif',
                           related_name='personne_physique_authmodif',
                           editable=False, null=True, blank=True)
    codecrea = CharField(max_length=200, null=True, blank=True)
    codemodif = CharField(max_length=200, null=True, blank=True)
    datecrea = DateTimeField(auto_now_add=True, null=True, blank=True)
    datemodif = DateTimeField(auto_now_add=True, null=True, blank=True)
    nom = CharField(max_length=200, null=True, blank=True)
    statut = IntegerField(default=0, null=True, blank=True)
    adresse1 = CharField(max_length=200, null=True, blank=True)
    adresse2 = CharField(max_length=200, null=True, blank=True)
    commentaire = CharField(max_length=200, null=True, blank=True)
    cp = CharField(max_length=200, null=True, blank=True)
    email = CharField(max_length=200, null=True, blank=True)
    euid = CharField(max_length=200, null=True, blank=True)
    fax = CharField(max_length=200, null=True, blank=True)
    pays = CharField(max_length=200, null=True, blank=True)
    tel = CharField(max_length=200, null=True, blank=True)
    tel2 = CharField(max_length=200, null=True, blank=True)
    ville = CharField(max_length=200, null=True, blank=True)
    web = CharField(max_length=200, null=True, blank=True)
    administrateur = IntegerField(default=0, null=True, blank=True)
    civilite = IntegerField(null=True, blank=True)
    key = CharField(max_length=200, null=True, blank=True)
    naissance = DateField(null=True, blank=True)
    prenom = CharField(max_length=200, null=True, blank=True)


class Employe(Model):

    class Meta:
        db_table = 'employe'

    user = ForeignKey(User, unique=True)

    uid = AutoField('ID', primary_key=True)
    authcrea = ForeignKey(User, db_column='authcrea',
                          related_name='employe_authcrea', editable=False,
                          null=True, blank=True)
    authmodif = ForeignKey(User, db_column='authmodif',
                           related_name='employe_authmodif', editable=False,
                           null=True, blank=True)
    codecrea = CharField(max_length=200, null=True, blank=True)
    codemodif = CharField(max_length=200, null=True, blank=True)
    datecrea = DateTimeField(auto_now_add=True, null=True, blank=True)
    datemodif = DateTimeField(auto_now_add=True, null=True, blank=True)
    nom = CharField(max_length=200, null=True, blank=True)
    statut = IntegerField(default=0, null=True, blank=True)
    adresse1 = CharField(max_length=200, null=True, blank=True)
    adresse2 = CharField(max_length=200, null=True, blank=True)
    commentaire = CharField(max_length=200, null=True, blank=True)
    cp = CharField(max_length=200, null=True, blank=True)
    email = CharField(max_length=200, null=True, blank=True, unique=True)
    euid = CharField(max_length=200, null=True, blank=True)
    fax = CharField(max_length=200, null=True, blank=True)
    pays = CharField(max_length=200, null=True, blank=True)
    tel = CharField(max_length=200, null=True, blank=True)
    tel2 = CharField(max_length=200, null=True, blank=True)
    ville = CharField(max_length=200, null=True, blank=True)
    web = CharField(max_length=200, null=True, blank=True)
    administrateur = IntegerField(default=0, null=True, blank=True)
    civilite = IntegerField(null=True, blank=True)
    key = CharField(max_length=200, null=True, blank=True)
    naissance = DateField(null=True, blank=True)
    prenom = CharField(max_length=200, null=True, blank=True)
    societe = ForeignKey(Societe, db_column='ref_societe')
    type_employe = ForeignKey(
        TypeEmploye, null=True, db_column='ref_type_employe')

    _root_notes_ids = None

    def root_notes_ids(self):
        if self._root_notes_ids is None:
            ids = set()
            curs = connection.cursor()
            if self.user.is_superuser:
                #curs.execute("select uid from note where statut=0 and ref_object=0")
                ids.add(0)
            else:
                curs.execute("select note.uid from droits, note where droits.ref_employe=%s"
                             " and droits.ref_note=note.uid and note.statut=0",
                             (self.uid,))
                for id, in curs.fetchall():
                    ids.add(id)
            self._root_notes_ids = ids
        return self._root_notes_ids

    _root_notes = None

    def root_notes(self):
        if self._root_notes is None:
            ids = list(self.root_notes_ids())
            self._root_notes = Note.objects.filter(uid__in=ids)
        return self._root_notes

    _root_notes_dj = None

    def root_notes_dj(self):
        """ returns the notes the user has 'droits' on."""
        if self._root_notes is None:
            droits = self.droits_set.all()
            notes_ids = self.user.is_superuser and [
                0] or [d.note_id for d in droits]
            self._root_notes = Note.valids.filter(uid__in=notes_ids)
        return self._root_notes

    def can_view(self, note):
        if self.user.is_superuser:
            return True
        for root_note in self.root_notes():
            if note.path.startswith(root_note.path):
                return True
        return False

    _workgroup_ids = None

    def workgroup_ids(self):
        if self._workgroup_ids is not None:
            return self._workgroup_ids
        ids = set()
        curs = connection.cursor()
        if self.user.is_superuser:
            curs.execute("select employe.uid from employe,auth_user where"
                         " employe.statut=0"
                         " and employe.uid!=0 and auth_user.id=employe.user_id"
                         " and auth_user.is_active")
            for id, in curs.fetchall():
                ids.add(id)
        else:
            for note in self.root_notes():
                curs.execute(
                    "select distinct employe.uid"
                    " from note,droits,employe,auth_user"
                    " where droits.ref_employe=employe.uid"
                    " and auth_user.id=employe.user_id"
                    " and auth_user.is_active"
                    " and droits.ref_note=note.uid and note.path like %s",
                    ('%s%%' % note.path,))
                for id, in curs.fetchall():
                    ids.add(id)
                curs.execute(
                    "select distinct ref_employe"
                    " from droits where ref_note=%s",
                    (note.uid,))
                for id, in curs.fetchall():
                    ids.add(id)
                ids.update(note.workgroup_ids())
        self._workgroup_ids = ids
        return self._workgroup_ids

    _workgroup = None

    def workgroup(self):
        if self._workgroup is None:
            ids = list(self.workgroup_ids())
            self._workgroup = Employe.objects.filter(uid__in=ids).exclude(
                uid=0).order_by('societe__nom', 'nom', 'prenom')
        return self._workgroup

    _workgroup_by_societe = None

    def workgroup_by_societe(self):
        if self._workgroup_by_societe is None:
            groups = []
            group_ids = []
            current_societe_id = None
            employes = []
            for employe in self.workgroup():
                if employe.societe_id != current_societe_id:
                    if current_societe_id:
                        societe = employes[0].societe
                        groups.append({'societe': societe,
                                       'employes': employes})
                        group_ids.append(societe.uid)
                        employes = []
                    current_societe_id = employe.societe_id
                employes.append(employe)
            if employes:
                societe = employes[0].societe
                groups.append({'societe': societe,
                               'employes': employes})
                group_ids.append(societe.uid)
            if self.user.is_superuser:
                for societe in Societe.objects.filter(statut=0).exclude(uid__in=group_ids):
                    groups.insert(0, {'societe': societe,
                                      'employes': []})

            self._workgroup_by_societe = groups
        return self._workgroup_by_societe

    def delete_droits(self):
        Droits.objects.filter(employe=self).delete()

    def __unicode__(self):
        if self.uid == 0:
            return u''
        return u'%s %s' % (self.prenom or '', self.nom or '')


class Type(Model):

    class Meta:
        db_table = 'type'

    uid = AutoField('ID', primary_key=True)
    authcrea = ForeignKey(User, db_column='authcrea',
                          related_name='type_authcrea', editable=False, null=True, blank=True)
    authmodif = ForeignKey(User, db_column='authmodif',
                           related_name='type_authmodif', editable=False, null=True, blank=True)
    codecrea = CharField(max_length=200, null=True, blank=True)
    codemodif = CharField(max_length=200, null=True, blank=True)
    datecrea = DateTimeField(auto_now_add=True, null=True, blank=True)
    datemodif = DateTimeField(auto_now_add=True, null=True, blank=True)
    nom = CharField(max_length=200, null=True, blank=True)
    statut = IntegerField(default=0, null=True, blank=True)


class EtatNote(Model):

    class Meta:
        db_table = 'etat_note'

    uid = AutoField('ID', primary_key=True)
    authcrea = ForeignKey(User, db_column='authcrea',
                          related_name='etat_note_authcrea', editable=False, null=True, blank=True)
    authmodif = ForeignKey(User, db_column='authmodif',
                           related_name='etat_note_authmodif', editable=False, null=True, blank=True)
    codecrea = CharField(max_length=200, null=True, blank=True)
    codemodif = CharField(max_length=200, null=True, blank=True)
    datecrea = DateTimeField(auto_now_add=True, null=True, blank=True)
    datemodif = DateTimeField(auto_now_add=True, null=True, blank=True)
    nom = CharField(max_length=200, null=True, blank=True)
    statut = IntegerField(default=0, null=True, blank=True)

    def __unicode__(self):
        return _(self.nom)


class TypeNote(Model):

    class Meta:
        db_table = 'type_note'

    uid = AutoField('ID', primary_key=True)
    authcrea = ForeignKey(User, db_column='authcrea',
                          related_name='type_note_authcrea', editable=False, null=True, blank=True)
    authmodif = ForeignKey(User, db_column='authmodif',
                           related_name='type_note_authmodif', editable=False, null=True, blank=True)
    codecrea = CharField(max_length=200, null=True, blank=True)
    codemodif = CharField(max_length=200, null=True, blank=True)
    datecrea = DateTimeField(auto_now_add=True, null=True, blank=True)
    datemodif = DateTimeField(auto_now_add=True, null=True, blank=True)
    nom = CharField(max_length=200, null=True, blank=True)
    statut = IntegerField(default=0, null=True, blank=True)

    def __unicode__(self):
        return self.nom


class Note(Model):

    class Meta:
        db_table = 'note'

    uid = AutoField('ID', primary_key=True)
    authcrea = ForeignKey(User, db_column='authcrea',
                          related_name='note_authcrea', editable=False, null=True, blank=True)
    authmodif = ForeignKey(User, db_column='authmodif',
                           related_name='note_authmodif', editable=False, null=True, blank=True)
    codecrea = CharField(max_length=200, null=True, blank=True)
    codemodif = CharField(max_length=200, null=True, blank=True)
    datecrea = DateTimeField(auto_now_add=True, null=True, blank=True)
    datemodif = DateTimeField(auto_now_add=True, null=True, blank=True)
    nom = CharField(null=True, blank=True, max_length=200)
    statut = IntegerField(default=0, null=True, blank=True)
    date_debut = DateTimeField(null=True, blank=True)
    date_fin = DateTimeField(null=True, blank=True)
    description = CharField(max_length=99999, null=True,
                            blank=True, verbose_name="Texte")
    montant = FloatField(null=True, blank=True, verbose_name="Durée")
    post_alarme = DateTimeField(null=True, blank=True)
    pre_alarme = DateTimeField(null=True, blank=True)
    priorite = IntegerField(null=True, blank=True)
    auteur_employe = ForeignKey(
        Employe, db_column='ref_auteur_employe', related_name='note_auteur_employe')
    demandeur_employe = ForeignKey(Employe, db_column='ref_demandeur_employe',
                                   related_name='note_demandeur_employe', verbose_name="Demandeur")
    etat_note = ForeignKey(EtatNote, db_column='ref_etat_note')
    parent = ForeignKey('self', db_column='ref_object')
    responsable_employe = ForeignKey(
        Employe, db_column='ref_responsable_employe',
        related_name='note_responsable_employe', verbose_name="Destinataire")
    type_note = ForeignKey(TypeNote, db_column='ref_type_note')
    resume = CharField(null=True, blank=True, max_length=400)
    reussite = IntegerField(null=True, blank=True)
    send_post_alarme = BooleanField(default=False,  blank=True)
    send_pre_alarme = BooleanField(default=False,  blank=True)
    path = CharField(max_length=200, null=True, blank=True)

    def priority_color(self):
        if not self.priorite or self.priorite < 3:
            return "green"
        if self.priorite < 6:
            return "blue"
        if self.priorite < 9:
            return "orange"
        return "red"


    def icon(self):
        type_note = self.type_note_id
        if type_note == 1: # département
            cl = 'home'
        elif type_note == 2: # dossier
            cl = 'folder'
        elif type_note == 3: # projet
            cl = 'folder'
        elif type_note == 4: # tâche
            cl = 'comment-o'
        elif type_note == 5: # rendez-vous
            cl = 'phone'
        elif type_note == 6: # bug
            cl = 'bug'
        elif type_note == 7: # souhait
            cl = 'question'
        elif type_note == 0: # indefini
            cl = 'comment'
        elif type_note == 8: # message
            cl = 'info'
        return cl



    def __unicode__(self):
        return "%s" % self.uid

    def save(self, *args, **kwargs):
        curs = connection.cursor()
        curs.execute(
            "INSERT into action (ref_object,authcrea,authmodif,codecrea,codemodif,datecrea,datemodif,nom,statut,date_debut,date_fin,description,montant,post_alarme,pre_alarme,priorite,ref_auteur_employe,ref_demandeur_employe,ref_etat_note,ref_responsable_employe,ref_type_note,resume,reussite,send_post_alarme,send_pre_alarme,path) select %s,authcrea,authmodif,codecrea,codemodif,datecrea,datemodif,nom,statut,date_debut,date_fin,description,montant,post_alarme,pre_alarme,priorite,ref_auteur_employe,ref_demandeur_employe,ref_etat_note,ref_responsable_employe,ref_type_note,resume,reussite,send_post_alarme,send_pre_alarme,path from note where uid=%s",
            (self.uid, self.uid))
        super(Note, self).save(*args, **kwargs)
        if not self.path:
            self.path = "%s/%s" % (self.parent.path, self.uid)
        else:
            parent_path_uid = self.path.split('/')[-1]
            if self.parent_id != 0 and str(self.parent_id) != parent_path_uid:
                self.path = "%s/%s" % (self.parent.path, self.uid)
        super(Note, self).save(*args, **kwargs)  # Pas cool

    def notify(self, sender=None, body=None, recipient_name=None):
        if settings.DEBUG:
            return
        if not sender:
            sender = self.authmodif
        if not recipient_name and self.responsable_employe_id:
            recipient = self.responsable_employe.user
            recipient_name = "[%s %s]" % (
                recipient.first_name, recipient.last_name)
        else:
            recipient_name = "[Tous]"

        recipients = User.objects.filter(id__in=self.workgroup_ids())
        subject = u"%s %s" % (recipient_name, self.resume)
        send_mail(sender, recipients, subject, body)

    def notify_modifs(self):
        previous = Action.objects.filter(object=self).order_by("-datemodif")

        if previous:
            previous = previous[0]
            body = note_diff(previous, self)
        else:
            body = note_diff(self, self)
        self.notify(body=body)

    def get_etat_note(self):
        return entities['etat_note'].get(self.etat_note_id)

    __attachments = None

    def attachments(self):
        if self.__attachments is None:
            self.__attachments = Attachment.objects.filter(
                note=self.uid, statut=0)
        return self.__attachments

    def __archive(self):
        pass

    def move(self, parent_note):
        pass

    def _set_path(self):
        pass

    def add_attachment(self):
        pass

    def del_attachment(self):
        pass

    _local_workgroup_ids = None

    def local_workgroup_ids(self):
        if self._local_workgroup_ids is None:
            curs = connection.cursor()
            ids = set([0])
            curs.execute("SELECT droits.ref_employe FROM droits,note WHERE"
                         " droits.ref_note=note.uid"
                         " AND note.statut=0 AND note.uid=%s",
                         (self.uid,))
            for id, in curs.fetchall():
                ids.add(id)
            self._local_workgroup_ids = ids
        return self._local_workgroup_ids

    _workgroup_ids = None

    def workgroup_ids(self):
        if self._workgroup_ids is None:
            ids = []
            curs = connection.cursor()
            path = self.path.split('/')
            path = filter(lambda x: x, path)
            note_in_path = map(lambda s: "note.uid=%s" % s, path)
            if path:
                query = "SELECT DISTINCT droits.ref_employe FROM droits, note WHERE" \
                    " droits.ref_note=note.uid" \
                    " AND note.statut=0" \
                    " AND (%s)" % " OR ".join(note_in_path)
                curs.execute(query)
                for id, in curs.fetchall():
                    ids.append(id)
            self._workgroup_ids = ids
        return self._workgroup_ids

    def add_user(self, authenticated_user, user):
        if not Droits.objects.filter(note=self, employe=user):
            droit = Droits(note=self, employe_id=user, type_role_id=0)
            droit.save()

    def del_user(self, user):
        Droits.objects.filter(note=self, employe=user).delete()


class Action(Model):

    class Meta:
        db_table = 'action'

    uid = AutoField('ID', primary_key=True)
    authcrea = ForeignKey(User, db_column='authcrea',
                          related_name='action_authcrea', editable=False, null=True, blank=True)
    authmodif = ForeignKey(User, db_column='authmodif',
                           related_name='action_authmodif', editable=False, null=True, blank=True)
    codecrea = CharField(max_length=200, null=True, blank=True)
    codemodif = CharField(max_length=200, null=True, blank=True)
    datecrea = DateTimeField(auto_now_add=True, null=True, blank=True)
    datemodif = DateTimeField(auto_now_add=True, null=True, blank=True)
    nom = CharField(max_length=200, null=True, blank=True)
    statut = IntegerField(default=0, null=True, blank=True)
    date_debut = DateTimeField(null=True, blank=True)
    date_fin = DateTimeField(null=True, blank=True)
    description = CharField(max_length=20000, null=True, blank=True)
    montant = FloatField(null=True, blank=True)
    post_alarme = DateTimeField(null=True, blank=True)
    pre_alarme = DateTimeField(null=True, blank=True)
    priorite = IntegerField(null=True, blank=True)
    auteur_employe = ForeignKey(
        Employe, db_column='ref_auteur_employe', related_name='action_auteur_employe')
    demandeur_employe = ForeignKey(
        Employe, db_column='ref_demandeur_employe', related_name='action_demandeur_employe')
    etat_note = ForeignKey(EtatNote, db_column='ref_etat_note')
    object = ForeignKey(Object, db_column='ref_object')
    responsable_employe = ForeignKey(
        Employe, db_column='ref_responsable_employe', related_name='action_responsable_employe')
    type_note = ForeignKey(TypeNote, db_column='ref_type_note')
    resume = CharField(max_length=200, null=True, blank=True)
    reussite = IntegerField(null=True, blank=True)
    send_post_alarme = BooleanField(default=False, blank=True)
    send_pre_alarme = BooleanField(default=False, blank=True)


class TypeRole(Model):

    class Meta:
        db_table = 'type_role'

    uid = AutoField('ID', primary_key=True)
    authcrea = ForeignKey(User, db_column='authcrea',
                          related_name='type_role_authcrea', editable=False, null=True, blank=True)
    authmodif = ForeignKey(User, db_column='authmodif',
                           related_name='type_role_authmodif', editable=False, null=True, blank=True)
    codecrea = CharField(max_length=200, null=True, blank=True)
    codemodif = CharField(max_length=200, null=True, blank=True)
    datecrea = DateTimeField(auto_now_add=True, null=True, blank=True)
    datemodif = DateTimeField(auto_now_add=True, null=True, blank=True)
    nom = CharField(max_length=200, null=True, blank=True)
    statut = IntegerField(default=0, null=True, blank=True)

    def __unicode__(self):
        return self.nom


class Droits(Model):

    class Meta:
        db_table = 'droits'

    uid = AutoField('ID', primary_key=True)
    employe = ForeignKey(Employe, db_column='ref_employe')
    note = ForeignKey(Note, db_column='ref_note')
    type_role = ForeignKey(TypeRole, db_column='ref_type_role')


class Timer(Model):

    class Meta:
        db_table = 'timer'
        unique_together = ('employe', 'note', 'effective_date')

    uid = AutoField('ID', primary_key=True)
    authcrea = ForeignKey(
        User, db_column='authcrea',
        related_name='timer_authcrea', editable=False,
        null=True, blank=True)
    authmodif = ForeignKey(
        User, db_column='authmodif',
        related_name='timer_authmodif', editable=False,
        null=True, blank=True)
    codecrea = CharField(max_length=200, null=True, blank=True)
    codemodif = CharField(max_length=200, null=True, blank=True)
    datecrea = DateTimeField(auto_now_add=True, null=True, blank=True)
    datemodif = DateTimeField(auto_now_add=True, null=True, blank=True)
    statut = IntegerField(default=0, null=True, blank=True)
    employe = ForeignKey(Employe, db_column='ref_employe')
    note = ForeignKey(Note, db_column='ref_note')
    duration = FloatField(default=0, null=True, blank=True)
    effective_date = DateField(auto_now_add=True, null=True, blank=True)


class Userid(Model):

    class Meta:
        db_table = 'userid'

    uid = AutoField('ID', primary_key=True)
    authcrea = ForeignKey(User, db_column='authcrea',
                          related_name='userid_authcrea', editable=False, null=True, blank=True)
    authmodif = ForeignKey(User, db_column='authmodif',
                           related_name='userid_authmodif', editable=False, null=True, blank=True)
    codecrea = CharField(max_length=200, null=True, blank=True)
    codemodif = CharField(max_length=200, null=True, blank=True)
    datecrea = DateTimeField(auto_now_add=True, null=True, blank=True)
    datemodif = DateTimeField(auto_now_add=True, null=True, blank=True)
    nom = CharField(max_length=200, null=True, blank=True)
    statut = IntegerField(default=0, null=True, blank=True)
    login = CharField(max_length=200, null=True, blank=True)
    pwd = CharField(max_length=200, null=True, blank=True)
    employe = ForeignKey(Employe, db_column='ref_employe')


fs = FileSystemStorage(location=settings.FS_STORAGE_PATH)


class Attachment(Model):

    class Meta:
        db_table = 'attachment'
    uid = AutoField('ID', primary_key=True)
    authcrea = ForeignKey(User, db_column='authcrea',
                          related_name='attachment_authcrea', editable=False, null=True, blank=True)
    authmodif = ForeignKey(User, db_column='authmodif',
                           related_name='attachment_authmodif', editable=False, null=True, blank=True)
    codecrea = CharField(max_length=200, null=True, blank=True)
    codemodif = CharField(max_length=200, null=True, blank=True)
    datecrea = DateTimeField(auto_now_add=True, null=True, blank=True)
    datemodif = DateTimeField(auto_now_add=True, null=True, blank=True)
    nom = CharField(max_length=200, null=True, blank=True)
    statut = IntegerField(default=0, null=True, blank=True)

    note = ForeignKey(Note, db_column='ref_note')
    source = FileField(upload_to='attachments', storage=fs)


classes = (
    Object, TypeEmploye, Personne, Societe, PersonnePhysique, Employe, Type,
    EtatNote, TypeNote, Note, Action, TypeRole, Droits, Userid, Attachment, Timer)


def get_request():
    for stack_record in inspect.stack():
        request = stack_record[0].f_locals.get('request')
        if request and getattr(request, 'user', None) \
           and isinstance(request.user, User):
            return request
    return None


def save_pim(sender, instance, signal, *args, **kwargs):
    now = datetime.datetime.now()
    code = "django:%s(%s)" % (
        os.path.basename(sys._getframe(5).f_code.co_filename), sys._getframe(5).f_code.co_name)
    instance.codemodif = code
    instance.datemodif = now
    request = get_request()
    if request:
        user = request.user
    else:
        user = None
    instance.authmodif = user
    if not instance.uid:
        curs = connection.cursor()
        curs.execute("select nextval('object_uid_seq')")
        uid = curs.fetchone()[0]
        instance.uid = uid
        instance.codecrea = code
        instance.datecrea = now
        instance.authcrea = user


def register():
    if not signals.pre_save.receivers:
        for classe in classes:
            signals.pre_save.connect(save_pim, sender=classe)

register()


class ValidManager(Manager):

    def get_query_set(self):
        return super(ValidManager, self).get_query_set().filter(statut=0)

for classe in classes:
    classe.add_to_class('valids', ValidManager())
