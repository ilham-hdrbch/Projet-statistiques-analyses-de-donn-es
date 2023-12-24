from django import forms
class UploadForm(forms.Form):
    filename = forms.FileField()
    column_name = forms.CharField()
    operation_choices = [('min', 'Min'), ('max', 'Max'), ('mode', 'Mode'), ('median', 'Median'), ('mean', 'Mean'),('sum', 'Somme'),
    ('std', 'Ecartype'),('etendu', 'Etendu'),]
    operation = forms.ChoiceField(choices=operation_choices)
    display_option_choices = [('head', 'Show Entire Head'), ('custom', 'Show Custom Range')]
    display_option = forms.ChoiceField(choices=display_option_choices)
    custom_lines = forms.CharField(required=False)




