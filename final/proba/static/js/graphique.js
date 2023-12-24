var selectedColumns = []; /* variable qui va recuperer les colonnes à tracer*/

function handleFileSelect(event) {
    /* Cette fonction permet de c ....*/
    const fileInput = event.target;
    const autresChamps = document.getElementById('autres_champs');
    const choixColonneContainer = document.getElementById('choix_colonne_container');

    if (fileInput.files.length > 0) {
        // Afficher les champs une fois que le fichier a été sélectionné
        autresChamps.classList.remove('hidden');

        // Charger les colonnes dans le champ de choix
        const file = fileInput.files[0];
        const reader = new FileReader();
        reader.onload = function (e) {
            const lines = e.target.result.split('\n');
            if (lines.length > 0) {
                const columns = lines[0].split(';');
                console.log(columns)
                choixColonneContainer.innerHTML = '';  // Effacer les options existantes

                for (const column of columns) {
                    const checkbox = document.createElement('input');
                    checkbox.type = 'checkbox';
                    checkbox.name = 'choix_colonne';
                    checkbox.value = column;
                    checkbox.id = `id_choix_colonne_${column}`;

                    const label = document.createElement('label');
                    label.htmlFor = `id_choix_colonne_${column}`;
                    label.appendChild(document.createTextNode(column));

                    choixColonneContainer.appendChild(checkbox);
                    choixColonneContainer.appendChild(label);
                    
                    checkbox.addEventListener('change', function () {
                        if (this.checked) {
                            selectedColumns.push(this.value);
                        } else {
                            const index = selectedColumns.indexOf(this.value);
                            if (index !== -1) {
                                selectedColumns.splice(index, 1);
                            }
                        }
                    });
                
                }
            }
        };

        reader.readAsText(file);
    } else {
        // Cacher les champs si aucun fichier n'est sélectionné
        autresChamps.classList.add('hidden');
    }
}

function addSelectedColumns() {
    /* Cette fonction permet d'ajouter la data des colonnes au formulaire vu que c'est un champ
    qui ne fai pas partie du modele forme qu'on à crée */
    const form = document.getElementById('form');
    

    // Ajoutez les colonnes sélectionnées en tant que champs supplémentaires au formulaire
    for (const column of selectedColumns) {
        const input = document.createElement('input');
        input.type = 'hidden';
        input.name = 'choix_colonne';
        input.value = column;
        form.appendChild(input);
    }
}
