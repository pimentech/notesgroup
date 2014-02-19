# -*- coding: utf-8 -*-
from rest_framework import serializers
from dj.notesgroup import models

class NGSerializer(serializers.ModelSerializer):
    def get_identity(self, data):
        try:
            return data.get('uid', None)
        except AttributeError:
            return None



class TreeListSerializer(NGSerializer):
    has_users = serializers.WritableField()
    has_subtree = serializers.WritableField()
    class Meta:
        model = models.Note
        fields = ('uid', 'nom', 'path', 'type_note')

    def to_native(self, obj):
        ret = super(TreeListSerializer, self).to_native(obj)
        ret['has_subtree'] = models.Note.objects.filter(
            parent=obj,
            etat_note__uid__lte=1,
            type_note__uid__lte=3).exists()
        ret['has_users'] = models.Droits.objects.filter(note=obj).exists()
        return ret


class NoteListSerializer(NGSerializer):
    class Meta:
        model = models.Note
        fields = ('uid', 'nom', 'path', 'statut', 'resume',
                  'date_debut', 'date_fin', 'reussite',
                  'demandeur_employe', 'responsable_employe',
                  'montant', 'priorite', 'etat_note', 'type_note')


class NoteSerializer(NGSerializer):
    class Meta:
        model = models.Note
        fields = ('uid', 'nom', 'path', 'statut', 'nom', 'resume',
                  'date_debut', 'date_fin', 'reussite',
                  'description', 'demandeur_employe', 'responsable_employe',
                  'montant', 'priorite', 'etat_note', 'type_note')
