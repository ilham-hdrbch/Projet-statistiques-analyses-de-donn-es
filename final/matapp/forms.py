from django import forms
class UploadForm(forms.Form):
    filename = forms.FileField()
    column_name1 = forms.CharField(required=False)
    column_name2 = forms.CharField(required=False)
    operation_choices = [('lineplot', 'lineplot'), ('scatterplot', 'scatterplot'),('boxplot', 'boxplot'),
                          ('hisplot', 'hisplot'),('kdeplot', 'kdeplot'), ('violinplot', 'violinplot'),
                          ('barplot', 'barplot'), ('heatmap', 'heatmap'),
                          ('Piechart', 'Piechart'), ('Countplot', 'Countplot')]
    operation = forms.ChoiceField(choices=operation_choices)
    

