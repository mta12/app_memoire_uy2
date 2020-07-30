from django.urls import path
from django.views.generic import TemplateView

from . import views


app_name = 'main'
urlpatterns = [
    path('search/', views.DocumentsResultsView.as_view(), name='searchDocs'),
    path('about-us/',
         TemplateView.as_view(template_name="main/about_us.html")),  # test -- Not OK
    path('', TemplateView.as_view(template_name="main/home.html")),  # test -- OK
    path('index/<int:pk>/', views.DocumentsDetailView.as_view(),
         name='detailsDocs'),  # test --
    path('index/<int:doc_id>/dwn/', views.download,
         name='downloadDocs'),  # test -- (si lien telechargement s'affiche ou pas, si possible de tel...)
    path('index/', views.DocumentsIndexView.as_view(),
         name='indexDocs'),  # test -- OK
]
