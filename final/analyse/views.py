from io import BytesIO, StringIO
from django.shortcuts import render, redirect
from django.http import HttpResponse
import numpy as np
import pandas as pd
from analyse.graphes_visualisations import*
from scipy.stats import norm, t
import matplotlib.pyplot as plt
import chardet

def importer_fichier2(request):

    if request.method == 'POST':
        fichier = request.FILES.get('fichier')
        encodings = [
            "ISO-8859-1",  # Latin-1
            "ISO-8859-15", # Latin-9
            "Windows-1252", # Commonly used in Windows systems
            "ISO-8859-2",  # Latin-2
            "ISO-8859-3",  # Latin-3
            "ISO-8859-4",  # Latin-4
            "ISO-8859-5",  # Latin/Cyrillic
            "ISO-8859-6",  # Latin/Arabic
            "ISO-8859-7",  # Latin/Greek
            "ISO-8859-8",  # Latin/Hebrew
            "ISO-8859-9",  # Latin-5
            "ISO-8859-10", # Latin-6
            "ISO-8859-11", # Latin/Thai
            "ISO-8859-13", # Latin-7
            "ISO-8859-14", # Latin-8
            "ISO-8859-16", # Latin-10
            ]
        if est_utf8(fichier) in encodings:
            return HttpResponse(f"L'encodage du fichier ({est_utf8(fichier)}) n'est pas supporté")
        else:
            pass
            
        if fichier:
            if fichier.name.endswith('.xlsx'):
                return HttpResponse("Veuillez uploader un fichier CSV.")
                # df = pd.read_excel(fichier)
            elif fichier.name.endswith('.csv'):
                df = pd.read_csv(fichier)
        else:
            return HttpResponse("Veuillez uploader un fichier CSV.")

        # Convertion le dataframe en HTML
        df_html = df.head().to_html(index=False, float_format='%.2f')

        # Stocker les noms de colonnes dans la session
        request.session['df_columns'] = df.columns.tolist()

        df_json = df.to_json()
        request.session['df_data'] = df_json

        # Création des cases à cocher pour les colonnes
        # checkboxes = ''.join([f'<input type="checkbox" name="col_checkbox" value="{col}" id="chk_{col}"><label for="chk_{col}">{col}</label><br>' for col in df.columns])
        # Création des boutons radio pour les colonnes
        radio_buttons = ''.join([f'<input type="radio" name="colonne" value="{col}" id="radio_{col}"><label for="radio_{col}">{col}</label><br>' for col in df.columns])

        operateurs = [
                '=', 
                '>',
                '<',
                '>=', 
                '<=', 
                '!='
            ]

        # Passage du HTML du dataframe et les cases à cocher au contexte
        context = {'df_html': df_html, 'radio_buttons': radio_buttons, 'operateurs': operateurs}

        return render(request, 'affichage.html', context)
              
    else:
        return render(request, 'upload1.html')
    
def appliquer_test_statistique(request):
    if 'submit_choix' in request.POST:
        if request.method == 'POST':
            colonne = request.POST.get('colonne')
             # Récupération le DataFrame stocké dans la session sous forme de JSON
            df_json = request.session.get('df_data')
            if df_json:
                # Reconstruction le DataFrame à partir de la chaîne JSON
                df = pd.read_json(StringIO(df_json))

                # Obtention toutes les valeurs de la colonne sélectionnée
                valeurs_colonne = df[colonne].tolist()
                    
        if not colonne:
            return HttpResponse("Aucune donnée de dataframe trouvée.")
        
        # Vérification si la taille de l'échantillon est supérieure ou égale à la taille de la population
        taille_echantillon = int(request.POST.get('taille_echantillon'))
        if taille_echantillon >= len(df):
            return HttpResponse("La taille de l'échantillon ne peut pas être supérieure ou égale au nombre total de lignes dans les données.", status=400)

        # Vérification si les valeurs de la colonne sont numériques
        if numerique_ou_non(valeurs_colonne) == False:
            return HttpResponse(f"Les valeurs de la colonne '{colonne}' ne peuvent pas être converties en numériques.", status=400)

        # Vérification si les valeurs sont NAN
        if df[colonne].isna().all(): 
            return HttpResponse(f"Toutes les valeurs de la colonne '{colonne}' sont NaN.", status=400)

        # colonne = request.POST.get('colonne')
        taille_echantillon = request.POST.get('taille_echantillon')
        h0_comparateur = request.POST.get('h0_comparateur')
        h0_valeur = request.POST.get('h0_valeur')
        ha_comparateur = request.POST.get('ha_comparateur')
        ha_valeur = request.POST.get('ha_valeur')
        alpha = request.POST.get('alpha')

        #---------------------------------------------------------------------------------------------------------------------
        
        # Conversion
        taille_echantillon = int(taille_echantillon)
        h0_valeur = float(h0_valeur)
        alpha = float(alpha)
        h0_comparateur = str(h0_comparateur)
        ha_comparateur = str(ha_comparateur)

        # Choix du test en fonction de la taille de l'échantillon
        # test = 'Z' if taille_echantillon >= 30 else 'T'

        if taille_echantillon >= 30 :

            test = 'Z'
            # Conversion de la liste en un tableau numpy
            valeurs_colonne_np = np.array(valeurs_colonne)

            # Extraction d'un échantillon aléatoire
            np.random.seed(0)
            echantillon = np.random.choice(valeurs_colonne_np, taille_echantillon, replace=False)

            # Calculer la moyenne de l'échantillon
            moy = (np.mean(echantillon))

            # Calculer l'écart-type de l'échantillon (utiliser la population std dev si connue)
            ecart_type = (np.std(echantillon, ddof=1))  # 'ddof=1' pour l'échantillon, utilisez 'ddof=0' pour la population

            # Calculer la statistique de test Z
            Z = (moy - h0_valeur) / (ecart_type / np.sqrt(taille_echantillon))

            # Déterminer le côté du test basé sur l'opérateur
            if ha_comparateur in ['=', '!=']:
            
                # Déterminer les scores Z critiques pour un test bilatéral
                Z_critique_negatif = norm.ppf(alpha / 2)  # Score Z critique à gauche
                Z_critique_positif = -Z_critique_negatif   # Score Z critique à droite (distribution symétrique)

                # Calculer la p-value pour un test bilatéral
                p_value = 2 * (1 - norm.cdf(np.abs(Z)))

                # Prendre une décision basée sur la p-value
                h0_rejected = p_value <= alpha

                context = {
                    'z_score': Z,
                    'z_critique_negatif': Z_critique_negatif,
                    'z_critique_positif': Z_critique_positif,
                    'p_value': p_value,
                    'h0_rejected': h0_rejected,
                    'image_base64': plot_bilateral(test, Z, Z_critique_negatif, Z_critique_positif, alpha, h0_rejected, p_value)
                }
                
                return render(request, 'resultat_test.html', context)

            elif ha_comparateur in ['>=', '>']:

                Z_critique = norm.ppf(1 - alpha)  # Score Z critique à droite
                p_value = 1 - norm.cdf(Z)
                h0_rejected = p_value <= alpha # Z > Z_critique

                context = {
                    'z_score': Z,
                    'z_critique': Z_critique,
                    'p_value': p_value,
                    'h0_rejected': h0_rejected,
                    'image_base64': plot_unilateral_droit(test, Z, Z_critique, alpha, h0_rejected, p_value)
                }

                return render(request, 'resultat_test.html', context)

            elif ha_comparateur in ['<=', '<']:

                Z_critique = norm.ppf(alpha)  # Score Z critique à gauche
                p_value = norm.cdf(Z)
                h0_rejected = p_value <= alpha # Z < Z_critique

                context = {
                    'z_score': Z,
                    'z_critique': Z_critique,
                    'p_value': p_value,
                    'h0_rejected': h0_rejected,
                    'image_base64': plot_unilateral_gauche(test, Z, Z_critique, alpha, h0_rejected, p_value)
                }

                return render(request, 'resultat_test.html', context)

            else:
                response_content = f"Colonne: {valeurs_colonne}, Taille échantillon: {taille_echantillon}, H0: µ {h0_comparateur} {h0_valeur}, HA: µ {ha_comparateur} {ha_valeur}, Alpha: {alpha}"
                return HttpResponse(response_content)
            
        else:
            test = 'T' 

            # Conversion de la liste en un tableau numpy
            valeurs_colonne_np = np.array(valeurs_colonne)

            # Extraction d'un échantillon aléatoire
            np.random.seed(0)
            echantillon = np.random.choice(valeurs_colonne_np, taille_echantillon, replace=False)

            # Calculer la moyenne de l'échantillon
            moy = (np.mean(echantillon))

            # Calculer l'écart-type de l'échantillon (utiliser la population std dev si connue)
            ecart_type = (np.std(echantillon, ddof=1))  # 'ddof=1' pour l'échantillon, utilisez 'ddof=0' pour la population

            # Calculer la statistique de test T et les degrés de liberté
            T = (moy - h0_valeur) / (ecart_type / np.sqrt(taille_echantillon))
            dofl = taille_echantillon - 1

            if ha_comparateur in ['=', '!=']:
            
                # Déterminer les scores T critiques pour un test bilatéral
                T_critique_negatif = t.ppf(alpha / 2, dofl)
                T_critique_positif = t.ppf(1 - alpha / 2, dofl)

                # Calculer la p-value pour un test bilatéral
                p_value = 2 * (1 - t.cdf(abs(T), dofl))

                # Prendre une décision basée sur la p-value
                h0_rejected = p_value <= alpha

                context = {
                    't_score': T,
                    't_critique_negatif': T_critique_negatif,
                    't_critique_positif': T_critique_positif,
                    'p_value': p_value,
                    'h0_rejected': h0_rejected,
                    'image_base64': plot_bilateral(test, T, T_critique_negatif, T_critique_positif, alpha, h0_rejected, p_value)
                }
                
                return render(request, 'resultat_test.html', context)
            
            elif ha_comparateur in ['>=', '>']:
            
                # Score T critique à droite
                T_critique = t.ppf(1 - alpha, dofl)

                # Calculer la p-value pour un test à droite
                p_value = 1 - t.cdf(T, dofl)

                # Prendre une décision basée sur la p-value
                h0_rejected = p_value <= alpha

                context = {
                    't_score': T,
                    't_critique': T_critique,
                    'p_value': p_value,
                    'h0_rejected': h0_rejected,
                    'image_base64': plot_unilateral_droit(test, T, T_critique, alpha, h0_rejected, p_value)
                }
                
                return render(request, 'resultat_test.html', context)
            
            elif ha_comparateur in ['<=', '<']:
            
                # Score T critique à gauche
                T_critique = t.ppf(alpha, dofl)

                # Calculer la p-value pour un test à gauche
                p_value = t.cdf(T, dofl)

                # Prendre une décision basée sur la p-value
                h0_rejected = p_value <= alpha

                context = {
                    't_score': T,
                    't_critique': T_critique,
                    'p_value': p_value,
                    'h0_rejected': h0_rejected,
                    'image_base64': plot_unilateral_gauche(test, T, T_critique, alpha, h0_rejected, p_value)
                }
                
                return render(request, 'resultat_test.html', context)



    else:
        return redirect('importer_fichier2')  # Rediriger vers la vue appropriée
    
    
def plot_bilateral(test, test_score, critique_negatif, critique_positif, alpha, h0_rejected, p_value):
    x = np.linspace(-4, 4, 1000)
    y = norm.pdf(x)

    plt.plot(x, y)
    plt.fill_between(x, 0, y, where=(x < critique_negatif) | (x > critique_positif), color='red', alpha=0.5)
    plt.fill_between(x, 0, y, where=(x > critique_negatif) & (x < critique_positif), color='blue', alpha=0.3)
    # plt.axvline(x=z_score, color='k', linestyle='dashed')
    plt.axvline(x=critique_negatif, color='r', linestyle='dotted')
    plt.axvline(x=critique_positif, color='r', linestyle='dotted')
    plt.title(f'Test {test} Bilatéral')
    plt.xlabel(f"Valeur {test}")
    plt.ylabel("Densité de Probabilité")
    plt.grid(True, which='both', linestyle='--', linewidth=0.5, color='gray', alpha=0.7)

    plt.legend(["ZNR", "ZR"], loc ="upper left")
    
    # Masquer les valeurs de l'axe Y
    # plt.yticks([])

    # plt.text(0, -0.06, f'Zone de Rejet pour alpha = {alpha}', ha='center', va='top', fontsize=10)

    decision = 'Rejeté' if h0_rejected else 'Non Rejeté'
    plt.annotate(f'{test} = {test_score:.2f}\n±{test}c = {critique_positif:.2f}\nH0: {decision}', xy=(0.75, 1.025), xycoords='axes fraction', 
                 fontsize=10, bbox=dict(boxstyle="round", alpha=0.1))

    buffer = BytesIO()
    plt.savefig(buffer, format='png', dpi=135)
    plt.close()
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    image_base64 = base64.b64encode(image_png).decode('utf-8')
    return image_base64

def plot_unilateral_droit(test, test_score, critique, alpha, h0_rejected, p_value):
    x = np.linspace(-4, 4, 1000)
    y = norm.pdf(x)

    plt.plot(x, y)
    plt.fill_between(x, 0, y, where=x > critique, color='red', alpha=0.5)
    plt.fill_between(x, 0, y, where=x < critique, color='blue', alpha=0.3)
    # plt.axvline(x=z_score, color='k', linestyle='dashed')
    plt.axvline(x=critique, color='r', linestyle='dotted')
    plt.title(f'Test {test} Unilatéral Droit')
    plt.xlabel(f"Valeur {test}")
    plt.ylabel("Densité de Probabilité")
    plt.grid(True, which='both', linestyle='--', linewidth=0.5, color='gray', alpha=0.7)

    plt.legend(["ZNR", "ZR"], loc ="upper left")

    # Masquer les valeurs de l'axe Y
    # plt.yticks([])

    # plt.text(0, -0.06, f'Zone de Rejet pour alpha = {alpha}', ha='center', va='top', fontsize=10)

    decision = 'Rejeté' if h0_rejected else 'Non Rejeté'
    plt.annotate(f'{test} = {test_score:.2f}\n{test}c = {critique:.2f}\nH0: {decision}', xy=(0.75, 1.025), xycoords='axes fraction', 
                 fontsize=10, bbox=dict(boxstyle="round", alpha=0.1))

    buffer = BytesIO()
    plt.savefig(buffer, format='png', dpi=135)
    plt.close()
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    image_base64 = base64.b64encode(image_png).decode('utf-8')
    return image_base64

def plot_unilateral_gauche(test, test_score, critique, alpha, h0_rejected, p_value):
    x = np.linspace(-4, 4, 1000)
    y = norm.pdf(x)

    plt.plot(x, y)
    plt.fill_between(x, 0, y, where=x < critique, color='red', alpha=0.5)
    plt.fill_between(x, 0, y, where=x > critique, color='blue', alpha=0.3)
    # plt.axvline(x=z_score, color='k', linestyle='dashed')
    plt.axvline(x=critique, color='r', linestyle='dotted')
    plt.title(f'Test {test} Unilatéral Gauche')
    plt.xlabel(f"Valeur {test}")
    plt.ylabel("Densité de Probabilité")
    plt.grid(True, which='both', linestyle='--', linewidth=0.5, color='gray', alpha=0.7)

    plt.legend(["ZNR", "ZR"], loc ="upper left")

    # plt.yticks([])

    # plt.text(0, -0.06, f'Zone de Rejet pour alpha = {alpha}', ha='center', va='top', fontsize=10)

    decision = 'Rejeté' if h0_rejected else 'Non Rejeté'
    plt.annotate(f'{test} = {test_score:.2f}\n{test}c = {critique:.2f}\nH0: {decision}', xy=(0.75, 1.025), xycoords='axes fraction', 
                 fontsize=10, bbox=dict(boxstyle="round", alpha=0.1))

    buffer = BytesIO()
    plt.savefig(buffer, format='png', dpi=135)
    plt.close()
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    image_base64 = base64.b64encode(image_png).decode('utf-8')
    return image_base64

def numerique_ou_non(lst):
    return all(isinstance(item, (int, float)) for item in lst)  

def est_utf8(file):
    file.seek(0)
    
    file_content = file.read(100000)
    result = chardet.detect(file_content)
    encoding = result['encoding']

    file.seek(0)
    
    return encoding




