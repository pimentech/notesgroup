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
    class Meta:
        model = models.Note
        fields = ('uid', 'nom', 'path', 'type_note')

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
