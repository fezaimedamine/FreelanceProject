import pandas as pd
import ast  # Pour convertir les chaînes en listes Python
import json  # Pour exporter les données au format JSON
from datetime import datetime

# Chargement des données
df_labels = pd.read_csv('liste_labels.csv')
df_labels['id_label'] = df_labels.index  # Ajout d'un identifiant unique pour chaque label

df_profiles = pd.read_csv('liste_artiste.csv')
df_profiles['id_profile'] = df_profiles.index  # Ajout d'un identifiant unique pour chaque artiste

# Conversion des chaînes de la colonne 'labels' en listes Python
df_profiles['labels'] = df_profiles['labels'].apply(ast.literal_eval)

# Explosion de la colonne 'labels' pour une correspondance 1 à 1
df_profiles_exploded = df_profiles.explode('labels')

print(df_profiles_exploded['labels'])  # Vérification de l'explosion des labels

# Normalisation des valeurs dans les deux colonnes
df_profiles_exploded['labels'] = df_profiles_exploded['labels'].str.strip().str.lower()
df_labels['label_name'] = df_labels['label_name'].str.strip().str.lower()

# Jointure entre les artistes et les labels
df_result = df_profiles_exploded.merge(
    df_labels, 
    left_on='labels', 
    right_on='label_name',  # Assurez-vous que cette colonne existe dans labels.csv
    how='inner'
)

# Sélection des colonnes finales
df_result = df_result[['id_profile', 'id_label']]

# Export des résultats vers des fichiers CSV
df_table_artist = df_profiles.iloc[:, :3]  # Assurez-vous que les 3 premières colonnes sont correctes
df_table_artist['id_artist'] = df_table_artist.index
df_table_artist.to_csv('table_artist.csv', index=False)

df_result.to_csv('table_relation.csv', index=False)

# Lecture du fichier CSV des relations sans l'argument 'index'
df_result = pd.read_csv('table_relation.csv')  # Suppression de index=False

# Ajout d'une colonne pour l'identifiant des relations
df_result['id_relation'] = df_result.index

# Conversion des DataFrames en dictionnaires pour l'export JSON
data_profile = df_table_artist.to_dict('records')
data_relation = df_result.to_dict('records')
data_labels=df_labels.to_dict('records')



# Export des données au format JSON
with open('table_artist.json', 'w') as f:
    json.dump(data_profile, f, indent=4)

with open('table_relation.json', 'w') as f:  # Correction du nom du fichier
    json.dump(data_relation, f, indent=4)

with open('table_labels.json', 'w') as f:  # Correction du nom du fichier
    json.dump(data_labels, f, indent=4)

ch="Export terminé : table_artist.csv, table_relation.csv, table_artist.json et table_relation.json"
print(ch)
with open('logfile.log', 'a') as error_file:
    error_file.write(f"{datetime.now()} - {str(ch)}\n")
