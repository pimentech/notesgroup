# -*- coding: utf-8 -*-
from rest_framework import serializers
from dj.notesgroup import models

class NGSerializer(serializers.ModelSerializer):

    def get_identity(self, data):
        try:
            return data.get('uid', None)
        except AttributeError:
            return None

class TimerSerializer(NGSerializer):

    class Meta:
        model = models.Timer
        fields = ('uid', 'duration')

class NoteListSerializer(NGSerializer):
    timer = serializers.WritableField()

    class Meta:
        model = models.Note
        fields = ('uid', 'nom', 'path', 'statut', 'resume',
                  'date_debut', 'date_fin', 'reussite',
                  'demandeur_employe', 'responsable_employe',
                  'montant', 'priorite', 'etat_note', 'type_note')

    def to_native(self, obj):
        ret = super(NoteListSerializer, self).to_native(obj)
        try:
            employe = self.context['request'].user.get_profile()
            form = self.context['view'].form
            date = form.cleaned_data.get('timer_date') or None
            timer = models.Timer.objects.get(
                note=obj,
                employe=employe,
                effective_date=date)
        except models.Timer.DoesNotExist:
            return ret
        ret['timer'] = TimerSerializer(timer).data
        return ret


class NoteSerializer(NGSerializer):

    class Meta:
        model = models.Note
        fields = ('uid', 'nom', 'path', 'statut', 'nom', 'resume',
                  'date_debut', 'date_fin', 'reussite',
                  'description', 'demandeur_employe', 'responsable_employe',
                  'montant', 'priorite', 'etat_note', 'type_note')
