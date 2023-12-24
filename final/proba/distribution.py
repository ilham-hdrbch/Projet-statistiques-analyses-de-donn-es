####################     importations     ####################
import base64
import numpy as np
import matplotlib
matplotlib.use('Agg') 
import seaborn as sns
from io import BytesIO
import matplotlib.pyplot as plt
from statistics import mean, median, mode


####################       fonctions        ####################

###### fonction 1
def bernoulli(data, fsize=(6, 4), couleur='skyblue'):
    variable = data.name.upper()
    plt.figure(figsize=fsize) # dim figure

    # courbe
    sns.histplot(data, kde=True, stat='probability', color=couleur, edgecolor='black', linewidth=1.2, binwidth=0.2)

    # label
    plt.xlabel(variable, fontsize=10)
    plt.title("Distribution de Bernoulli", fontsize=12)


    # Convertir la figure en une chaîne base64 pour afficher en image
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_data = base64.b64encode(buffer.read()).decode()
    plt.close()

    # Retourner la chaîne base64 pour affichage dans le modèle
    return f'<img src="data:image/png;base64,{image_data}" alt="Graphique">'



###### fonction 2
def binomiale(data, fsize=(6, 4), couleur='skyblue'):
    variable = data.name.upper()
    plt.figure(figsize=fsize)

    
    ax = sns.histplot(data, kde=True, stat='probability', color=couleur, edgecolor='black', linewidth=1.2)
    ax.set(xlabel=variable)
    plt.title("Distribution de Binomiale", fontsize=12)

    # Convertir la figure en une chaîne base64 pour afficher en image
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_data = base64.b64encode(buffer.read()).decode()
    plt.close()

    # Retourner la chaîne base64 pour affichage dans le modèle
    return f'<img src="data:image/png;base64,{image_data}" alt="Graphique">'



###### fonction 3
def uniforme(data, fsize=(6, 4), couleur='skyblue'):
    variable = data.name.upper()
    try:
        plt.figure(figsize=fsize)

        # Tracer, labels
        sns.histplot(data, kde=True, color=couleur, fill=False, label='Densité de probabilité')
        plt.xlabel(variable)
        plt.title('Densité de Probabilité de la Distribution Uniforme', fontsize=12)

        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_data = base64.b64encode(buffer.read()).decode()
        plt.close()

        return f'<img src="data:image/png;base64,{image_data}" alt="Graphique">'
    except Exception as e:
        print(f"Erreur dans la fonction uniform_density_plot : {e}")
        return None



###### fonction 4
def poisson(data, fsize=(6, 4), couleur='skyblue', binwidth=0.1):
    variable = data.name.upper()
    try:
        plt.figure(figsize=fsize)


        plt.hist(data, bins=np.arange(min(data), max(data) + binwidth, binwidth), density=True, color=couleur, edgecolor='black', linewidth=1.2)

        # l'estimation de densité de noyau (KDE) avec sns.kdeplot
        sns.kdeplot(data, color='red', linestyle='--')

        # labels
        plt.xlabel(variable)
        plt.title('Distribution de Poisson', fontsize=12)

        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_data = base64.b64encode(buffer.read()).decode()
        plt.close()

        return f'<img src="data:image/png;base64,{image_data}" alt="Graphique">'
    except Exception as e:
        print(f"Erreur dans la fonction poisson_matplotlib : {e}")
        return None



###### fonction 5
def normale(data, fsize=(6, 4), couleur='skyblue'):
    variable = data.name.upper()
    try:
        plt.figure(figsize=fsize)

        sns.kdeplot(data, color=couleur, fill=True, label='Densité de probabilité')

        # moyenne, la médiane et le mode
        moyenne = mean(data)
        mediane = median(data)
        try:
            mode_val = mode(data)
        except e:
            mode_val = "Mode indéfini"

        # Annoter la moyenne, la médiane et le mode sur le graphique
        plt.axvline(moyenne, color='green', linestyle='--', label=f'Moyenne: {moyenne:.2f}')
        plt.axvline(mediane, color='orange', linestyle='--', label=f'Médiane: {mediane:.2f}')
        plt.axvline(mode_val, color='red', linestyle='--', label=f'Mode: {mode_val}')

        plt.xlabel(variable)
        plt.title('Densité de Probabilité de la Distribution Normale', fontsize=12)
        plt.legend()

        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_data = base64.b64encode(buffer.read()).decode()
        plt.close()

        return f'<img src="data:image/png;base64,{image_data}" alt="Graphique">'
    except Exception as e:
        print(f"Erreur dans la fonction normale_density_plot_with_stats : {e}")
        return None


###### onction 6
def exponentielle(data, fsize=(6, 4), couleur='skyblue'):
    variable = data.name.upper()
    try:
        plt.figure(figsize=fsize)

        sns.kdeplot(data, color=couleur, fill=True, label='Densité de probabilité')

        # moyenne
        moyenne = mean(data)

        # Annoter la moyenne sur le graphique
        plt.axvline(moyenne, color='green', linestyle='--', label=f'Moyenne: {moyenne:.2f}')
    
        plt.xlabel(variable)
        plt.title('Densité de Probabilité de la Distribution Exponentielle', fontsize=12)
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_data = base64.b64encode(buffer.read()).decode()
        plt.close()

        return f'<img src="data:image/png;base64,{image_data}" alt="Graphique">'
    except Exception as e:
        print(f"Erreur dans la fonction exponentielle_density_plot : {e}")
        return None
