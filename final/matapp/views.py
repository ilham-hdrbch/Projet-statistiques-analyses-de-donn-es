from django.http import HttpResponse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import urllib.parse
import base64
import io
from django.shortcuts import render
from .forms import UploadForm

def upload(request):
    form = UploadForm()
    result_display = None
    data_uri = None

    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)

        if form.is_valid():
            uploaded_file = form.cleaned_data.get('filename')

            if uploaded_file:
                try:
                    if uploaded_file.name.endswith('.csv'):
                        df = pd.read_csv(uploaded_file)
                    elif uploaded_file.name.endswith('.xlsx'):
                        df = pd.read_excel(uploaded_file)
                    else:
                        return HttpResponse('Format de fichier non pris en charge. Veuillez télécharger un fichier CSV ou Excel.')

                    column_types = df.dtypes
                    numeric_columns = column_types[column_types.apply(lambda x: np.issubdtype(x, np.number))].index
                    categorical_columns = column_types[column_types == 'object'].index

                    column_name1 = form.cleaned_data['column_name1']
                    column_name2 = form.cleaned_data['column_name2']
                    operation = form.cleaned_data['operation']

                    if operation == 'lineplot':
                        if column_name1 not in numeric_columns or column_name2 not in numeric_columns:
                            return HttpResponse('Les colonnes sélectionnées doivent être numériques pour un Line Plot.')
                        else:
                            plt.figure(figsize=(10, 6))
                            sns.lineplot(x=column_name1, y=column_name2, data=df, marker='o', color='b', label='V')
                            plt.xlabel(column_name1)
                            plt.ylabel(column_name2)
                            plt.title(f"Line Plot of {column_name1} and {column_name2}")

                    elif operation == 'scatterplot':
                        if column_name1 not in numeric_columns or column_name2 not in numeric_columns:
                            return HttpResponse('Les colonnes sélectionnées doivent être numériques pour un scatter Plot.')
                        else:
                        # Create a scatter plot
                            plt.figure(figsize=(10, 6))
                            sns.scatterplot(x=column_name1, y=column_name2, data=df, marker='o', color='b', label='V')
                            plt.xlabel(column_name1)
                            plt.ylabel(column_name2)
                            plt.title(f"Scatter Plot of {column_name1} vs {column_name2}")

                    elif operation == 'boxplot':
                        if column_name2 not in numeric_columns or column_name1 not in categorical_columns :
                            return HttpResponse('Les colonnes sélectionnées doivent être x catégorique et y numériques pour un Box Plot.')
                        else:
                            # Create a scatter plot
                            plt.figure(figsize=(10, 6))
                            #sns.boxplot(x=column_name1, y=column_name2, data=df, marker='o', color='b', label='V')
                            sns.boxplot(x=column_name1, y=column_name2, data=df)
                            plt.xlabel(column_name1)
                            plt.ylabel(column_name2)
                            plt.title(f"Box Plot of {column_name1} vs {column_name2}")
                        
                            

                    elif operation == 'hisplot':
                        if column_name1 not in numeric_columns:
                            return HttpResponse('La colonne sélectionnée doit être  numériques pour un Histogram Plot.')
                        else:
                            sns.set()  # or sns.set(style="whitegrid")
                            plt.figure(figsize=(10, 6))
                            sns.histplot(data=df, x=column_name1)
                            plt.xlabel(column_name1)
                            plt.ylabel("Count")
                            plt.title(f"Histogram of {column_name1}")
                    
                    elif operation == 'kdeplot':
                        if column_name1 not in numeric_columns:
                            return HttpResponse('La colonne sélectionnée doit être  numériques pour un KDE Plot.')
                        else:
                            sns.set()  # or sns.set(style="whitegrid")
                            plt.figure(figsize=(10, 6))
                            sns.kdeplot(data=df, x=column_name1, fill=True)
                            plt.xlabel(column_name1)
                            plt.ylabel("Density")
                            plt.title(f"KDE of {column_name1}")
                    
                    elif operation == 'violinplot':
                        sns.set()  # or sns.set(style="whitegrid")
                        plt.figure(figsize=(10, 6))
                        sns.violinplot(data=df, x=column_name1)
                        plt.xlabel(column_name1)
                        plt.title(f"Violin of {column_name1}")

                    elif operation == 'barplot':
                        if  column_name2 not in numeric_columns:
                            return HttpResponse('Les colonnes sélectionnées doivent être x catégorique ou numérique et y numériques pour un Bar Plot.')
                        else:
                            sns.set()  # or sns.set(style="whitegrid")
                            plt.figure(figsize=(10, 6))
                            sns.barplot(data=df, x=column_name1, y=column_name2)
                            plt.xlabel(column_name1)
                            plt.ylabel(column_name2)
                            plt.title(f"Bar plot of {column_name1} and {column_name2}")

                    elif operation == 'heatmap':
                        df_num = df.select_dtypes(include=['number'])
                        sns.heatmap(df_num.corr())
                        plt.title(f" Heatmap:")

                    elif operation == 'Piechart':
                        if column_name1 not in categorical_columns:
                            return HttpResponse('La colonne sélectionnée pour le Pie Chart doit être catégorique.')

                        plt.figure(figsize=(10, 6))
                        
                        # Get counts for each category in the selected column
                        counts = df[column_name1].value_counts()
                        
                        # Extract labels and values for the pie chart
                        labels = counts.index
                        values = counts.values
                        
                        plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=140)
                        plt.title(f"Pie Chart of {column_name1}")

                    elif operation == 'Countplot':
                        if  column_name1 not in categorical_columns:
                            return HttpResponse('La colonne sélectionnée doit être catégorique  pour un Count Plot.')
                        else:
                            sns.set()  # or sns.set(style="whitegrid")
                            plt.figure(figsize=(10, 6))
                            sns.countplot(data=df, x=column_name1)
                            plt.xlabel(column_name1)
                            plt.ylabel("Count")
                            plt.title(f"Count plot of {column_name1}")


                    # Save the plot to a buffer
                    buf = io.BytesIO()
                    plt.savefig(buf, format='png')
                    buf.seek(0)

                    # Convert the plot to base64 and encode it
                    string = base64.b64encode(buf.read()).decode('utf-8')
                    data_uri = urllib.parse.quote(string)

                    # Close the plot
                    plt.close()

                    #result_display = "Calcul réussi !"

                except (pd.errors.EmptyDataError, pd.errors.ParserError, KeyError, AttributeError) as e:
                    result_display = f"Error processing file: {str(e)}"

    return render(request, 'upload.html', {'form': form, 'data': data_uri, 'result_display': result_display})

