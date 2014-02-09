from django.contrib import admin
from django import forms
from dj.notesgroup import models
from django.template.defaultfilters import timesince
# from django.contrib.admin.filterspecs import RelatedFilterSpec, FilterSpec



# class WorkgroupFilterSpec(RelatedFilterSpec):
#     def __init__(self, f, request, params, model, model_admin):
#         super(WorkgroupFilterSpec, self).__init__(f, request, params, model, model_admin)

#         if not request.user.is_superuser:
#             self.lookup_choices = [ (id, name) \
#                     for (id, name) in self.lookup_choices \
#                     if id in request.user.get_profile().workgroup_ids()
#                     ]

# FilterSpec.filter_specs.insert(0, (lambda f: bool(f.name in ('demandeur_employe', 'responsable_employe')), WorkgroupFilterSpec) )



class AttachmentForm(forms.ModelForm):

    class Meta:
        model = models.Attachment
        fields = ('source',)

class AttachmentInline(admin.TabularInline):
    model = models.Attachment
    form = AttachmentForm
    extra = 1



class NoteForm(forms.ModelForm):
    description = forms.CharField(required=False, widget=forms.Textarea)

    class Meta:
        model = models.Note

    def __init__(self, *args, **kwargs):
        super(NoteForm, self).__init__(*args, **kwargs)

        if self.instance:
            self.fields['demandeur_employe'] = forms.ModelChoiceField(
                    queryset=models.Employe.objects.filter(uid__in=self.instance.workgroup_ids())
                    )
            self.fields['responsable_employe'] = forms.ModelChoiceField(
                    queryset=models.Employe.objects.filter(uid__in=self.instance.workgroup_ids())
                    )


class NoteAdmin(admin.ModelAdmin):

    date_hierarchy = 'datemodif'

    form = NoteForm

    fieldsets =(
            ("Metas", {
                'fields': ('nom', 'resume', ('demandeur_employe', 'responsable_employe'), 'priorite', 'montant', ),
                }),
            ('Speak.', {
                'fields': ('description', )
                }),
            ('Ninja Fields', {
                'classes': ('collapse',),
                'fields': ('etat_note', 'type_note', )
                }),
            )

    list_display = ('resume', 'nom', 'demandeur_employe', "responsable_employe", 'timesince_datemodif', "priorite", "montant", 'etat_note')

    list_display_links = ('resume', 'nom', )

    #list_editable = ()

    list_filter = ('etat_note', 'demandeur_employe', "responsable_employe", )

    search_fields = ['nom', 'resume', 'description']

    inlines = [ AttachmentInline ]

    def queryset(self, request):
        qs = super(NoteAdmin, self).queryset(request)
        qs = qs.select_related('demandeur_employe', 'responsable_employe', 'etat_note', 'type_note', )
        return qs

    def timesince_datemodif(self, obj):
        return timesince(obj.datemodif)
    timesince_datemodif.admin_order_field = 'datemodif'


admin.site.register(models.Note, NoteAdmin)









