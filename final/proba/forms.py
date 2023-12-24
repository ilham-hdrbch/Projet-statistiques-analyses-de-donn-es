from django import forms

class Formulaire(forms.Form):
    fichier_csv = forms.FileField(label="Fichier CSV", help_text="Sélectionnez un fichier CSV", widget=forms.FileInput(attrs={'accept': '.csv'}))
    choix_distribution = forms.ChoiceField(
        label="Choisissez une distribution",
        choices=[
            ('option1', 'Normale'),
            ('option2', 'Exponentielle'),
            ('option3', 'Poisson'),
            ('option4', 'Uniforme'),
            ('option5', 'Binomiale'),
            ('option6', 'Bernoulli'),
        ],
        widget=forms.Select(attrs={'id': 'choix_distribution'})
    )
