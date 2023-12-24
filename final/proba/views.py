################################################       importations       ###############################################
import pandas as pd
from io import StringIO
from .forms import Formulaire
from django.shortcuts import render
from django.http import HttpResponse
from .distribution import poisson, bernoulli, binomiale, normale, exponentielle, uniforme
################################################ fonctions personnelles dev ################################################

# aucune

################################################        les vues          ################################################

# vue 1
def upload_file(request):
    
    if request.method == 'POST':
        formulaire = Formulaire(request.POST, request.FILES)
        if formulaire.is_valid():
            colonnes = request.POST.getlist('choix_colonne') # liste des colonne selectionées
            fichier_csv = request.FILES['fichier_csv'] # fichier csv
            # recuperation de la distribution selectionnée
            choix_distribution_value = formulaire.cleaned_data['choix_distribution']
            distribution = dict(formulaire.fields['choix_distribution'].choices).get(choix_distribution_value) 
            print(colonnes, distribution,fichier_csv)

            return generer_graphique(request, fichier_csv=fichier_csv, distribution=distribution, colonnes=colonnes)
        
    # Si la méthode de requête n'est pas POST, créez une instance du formulaire vide (GET)
    else:
        formulaire = Formulaire() # revois un formulaire vide

    # Mettez à jour le contexte avec le formulaire
    context = {'formulaire': formulaire}
    # Renvoyez le formulaire à la page (graphique.html dans cet exemple)
    return render(request, 'graphique.html', context)





# Vue pour la page graphique
def generer_graphique(request, fichier_csv, distribution, colonnes):
    dict_distribution = {
        "bernoulli": bernoulli,
        "poisson": poisson, 
        "bernoulli": bernoulli, 
        "binomiale": binomiale, 
        "normale": normale, 
        "exponentielle": exponentielle, 
        "uniforme": uniforme
        }

    fichier_csv_content = fichier_csv.read().decode('utf-8') # le texte en dure
    
    # Lecture du fichier CSV avec pandas
    try:
        dataframe = pd.read_csv(StringIO(fichier_csv_content), sep=";")
        liste_graphe = []
        for col in colonnes:
            liste_graphe.append(dict_distribution[distribution.lower()](dataframe[col]))

        # Mettez à jour le contexte avec les informations du formulaire et le chemin de l'image
        context = {
            'fichier_csv_info': f"Nom du fichier CSV : {fichier_csv.name}",
            'choix_distribution_info': f"Choix de distribution : {distribution}",
            'liste_graphe': liste_graphe
            }

        # Renvoyez le résultat à la page graphique.html
        return render(request, 'graphique.html', context)
    except pd.errors.EmptyDataError:
        # Gérez le cas où le fichier CSV est vide
        return HttpResponse("Le fichier CSV est vide.")
    except pd.errors.ParserError:
        # Gérez le cas où il y a une erreur lors de l'analyse du fichier CSV
        return HttpResponse("Erreur lors de l'analyse du fichier CSV.")
