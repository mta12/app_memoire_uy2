import datetime

from django.shortcuts import render, get_object_or_404
from django.views import generic  # P287
from django.urls import reverse
from django.utils import timezone
from django.http import HttpResponse
from django.db.models import Q

import main.models as m

# Create your views here.

# Afficher la liste des documents publiés récemments


class DocumentsIndexView(generic.ListView):
    paginate_by = 6
    template_name = 'main/docs/index_documents.html'
    context_object_name = 'latest_document_list'

    def get_queryset(self):
        """
        Retourne les documents récents dans un delai d'une semaine
           """
        return m.Document.objects.filter(
            pub_date__lte=timezone.now(),
            pub_date__gt=timezone.now() - datetime.timedelta(m.LIMIT_DAYS),
        ).order_by('-pub_date')  # [:10]

# class DocumentQuerySet() 06:55 dans les modèles


class DocumentsResultsView(generic.ListView):
    paginate_by = 6
    count = 0

    model = m.Document
    template_name = 'main/docs/search_documents.html'
    # A appeler apres la saisie et la validation dans le champ de recherche

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['count'] = self.count or 0
        context['query'] = self.request.GET.get('q')
        return context

    def get_queryset(self):
        # rechercher sur toute la requete
        query = self.request.GET.get('q', None)

        if query is not None:
            doc_results = m.Document.objects.search(query)
            self.count = len(doc_results)
            return doc_results
        return m.Document.objects.none()


# class DocumentsResultsView(generic.ListView):
#     paginate_by = 6

#     model = m.Document
#     template_name = 'main/docs/search_documents.html'
#     # A appeler apres la saisie et la validation dans le champ de recherche

#     def get_queryset(self):
#         list1 = []
#         query = self.request.GET.get('q')  # rechercher sur toute la requete
#         # rechercher sur chaque element de la liste
#         queries = str(query).split(" ")

#         document_list = m.Document.objects.filter(
#             titre_doc__icontains=query)  # Tous les résultats doivent être uniques
#         # Ajout de la seconde recherche dans la liste
#         # list1.append(recherche_avec_liste_elements(cles=queries))

#         # le set garantit qu'on aura que des éléments uniques
#         #document_list = list(set(list1))

#         return document_list


class DocumentsDetailView(generic.DetailView):  # P656
    model = m.Document
    template_name = 'main/docs/details_document.html'

    def get_queryset(self):
        """
        Retourne les 10 documents récents dans un delai d'une semaine
           """
        return m.Document.objects.filter(
            pub_date__lte=timezone.now(),
            pub_date__gt=timezone.now() - datetime.timedelta(m.LIMIT_DAYS),
        )

# vue qui gère le telechargement d'un fichier


def download(request, doc_id):  # Refléchir dessus à tete reposée
    print("docs id ", doc_id)
    doc = get_object_or_404(m.Document, pk=doc_id)
    fic = doc.fichier
    response = HttpResponse(content_type='application/vnd.pdf')
    response['Content-Disposition'] = f'attachment; filename="{fic.name}"'
    return response  # de django.http
