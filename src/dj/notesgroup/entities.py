# -*- coding: utf-8 -*-
from django_pimentech.dbhandler import EntityDict, EntityRDict, entities, rentities
from django.utils.translation import ugettext_lazy as _

tablenames = [ 'etat_note', 'type_note' ]


class EntityDictTrad(EntityDict):
    def load(self, tablename):
        data = self.execute(self.SELECT % tablename).fetchall()
        if not data:
            raise self.DoesNotExist, self.SELECT % tablename
        self.__keys = [ key for (key, value) in data ]
        data = [ (key, _(value)) for (key, value) in data ]
        self.data = dict(data)


for tablename in tablenames:
    entities[tablename] = EntityDictTrad(tablename)
    rentities[tablename] = EntityRDict(tablename)
