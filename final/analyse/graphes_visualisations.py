import io
import base64
import seaborn as sns 
import pandas as pan 
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from django.shortcuts import render
from django.http import HttpResponse

def line_plot(df_colonnes):
    try:
        # Supposons que 'df' est votre DataFrame
        # Exemple d'une opération qui pourrait générer une exception
        les_colonnes = df_colonnes.columns.tolist()
        
        sns.set_theme()
        # Créer un Line Plot
        sns.lineplot(x= les_colonnes[0], y= les_colonnes[1], data=df_colonnes)

        # Enregistrer le graphique dans un tampon en mémoire
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        # Fermer le graphique pour libérer la mémoire
        plt.close()
        buffer.seek(0)

        image_png = buffer.getvalue()
        buffer.close()

        # Encoder l'image en base64
        image_base64 = base64.b64encode(image_png)
        image_base64 = image_base64.decode('utf-8')

        # Retourner la chaîne encodée
        return image_base64

        # Retourner l'image comme réponse HTTP
        # return HttpResponse(buffer.getvalue(), content_type='image/png')
        

    except ValueError as e:
        # Gérer ValueError et retourner une réponse HTTP appropriée
        return HttpResponse("Erreur. Le type de la valeur donnée n'est pas compatible avec ce graphe ")

    except TypeError as e:
        # Gérer TypeError et retourner une réponse HTTP appropriée
        return HttpResponse("Erreur. Le type de la valeur donnée n'est pas compatible avec ce graphe ")
    
    except Exception as e:
        return HttpResponse(f"Une erreur s'est produite : {e}")
