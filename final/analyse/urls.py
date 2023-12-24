from django.urls import path
from .import views

app_name = 'analyse'
urlpatterns = [
    path('importer_fichier2/', views.importer_fichier2, name="importer_fichier2"),
    # path('traitement_affichage/<colonnes>/<graphe>/', views.traitement_affichage, name='traitement_affichage'),
    # path('traitement_affichage/', views.traitement_affichage, name="traitement_affichage"),
    path('appliquer_test_statistique/', views.appliquer_test_statistique, name="appliquer_test_statistique")
]
