from django.contrib import admin
from .models import Personne, Enseignant, Etudiant
from . import models
# Register your models here.

admin.site.register(Personne)
admin.site.register(Enseignant)
admin.site.register(Etudiant)


class DocumentAdmin(admin.ModelAdmin):
    list_display = ('type_doc', 'titre_doc', 'auteur',
                    'date_selection', 'pub_date', 'fichier')
    list_filter = ('date_selection', 'est_soutenu', 'date_soutenance',)
    search_fields = ('auteur', 'titre_doc', 'resume_doc',
                     'etablissement', 'type_formation')
    # Pour définir l'heure actuelle on peut utiliser django.utils.timezone.now()

    fieldsets = (
        ('Le Document', {
            "fields": (
                'type_doc', 'titre_doc', 'resume_doc', 'fichier', 'est_soutenu',
                'note_soutenance',
            ),
        }),
        ('Auteur', {
            "fields": (
                'auteur', 'filiere', 'type_formation', 'etablissement',
            ),
        }),
        ('Les dates', {
            "fields": (
                'date_selection', 'date_soutenance', 'pub_date',
            ),
        }),
        ('Encadreur', {
            "fields": (
                'encadreur',
            ),
        }),
        ('Membres du Jury', {
            "fields": (
                'jury',
            ),
        }),
    )


admin.site.register(models.Document, DocumentAdmin)
