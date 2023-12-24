from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
from .forms import UploadForm

def statistics(request):
    form = UploadForm()
    df_head_display = None
    result_display = None

    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)

        if form.is_valid():
            uploaded_file = form.cleaned_data.get('filename')

            if uploaded_file:
                if uploaded_file.name.endswith('.csv'):
                    df = pd.read_csv(uploaded_file)
                elif uploaded_file.name.endswith('.xlsx'):
                    df = pd.read_excel(uploaded_file)
                else:
                    return HttpResponse('Format de fichier non pris en charge. Veuillez télécharger un fichier CSV ou Excel.')

                # Display df.head() or custom range on the same page
                display_option = form.cleaned_data['display_option']
                if display_option == 'head':
                    df_head_display = df.head().to_html()
                elif display_option == 'custom':
                    custom_lines = form.cleaned_data['custom_lines']
                    try:
                        start, end = map(int, custom_lines.split(':'))
                        df_head_display = df.iloc[start:end+1].to_html()
                    except (ValueError, IndexError):
                        df_head_display = "Veuillez entrer un intervalle valide."

                # Perform operation
                column_name = form.cleaned_data['column_name']
                operation = form.cleaned_data['operation']

                try:
                    if operation == 'mode':
                        result = df[column_name].mode()
                    elif operation == 'median':
                        result = df[column_name].median()
                    elif operation == 'mean':
                        result = df[column_name].mean()
                    elif operation == 'sum':
                        result = df[column_name].sum()
                    elif operation == 'std':
                        result = df[column_name].std()
                    elif operation == 'etendu':
                        result = df[column_name].max() - df[column_name].min()
                    else:
                        result = getattr(df[column_name], operation)()
                
                    result_display = f"le {operation} de le colonne'{column_name}' est: {result}"
                except (KeyError, AttributeError):
                    result_display = f"Invalid column name: {column_name}"

    return render(request, 'statistics.html', {'form': form, 'df_head_display': df_head_display, 'result_display': result_display})

