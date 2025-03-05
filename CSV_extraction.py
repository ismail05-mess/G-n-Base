# -*- coding: utf-8 -*-
import csv
import uuid
from datetime import datetime

def extract_column(file_path, column_index):
    column = []
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # passer l'entête
        for row in reader:
            # On vérifie qu'on a assez de colonnes sinon on ajoute une chaîne vide
            if len(row) > column_index:
                column.append(row[column_index])
            else:
                column.append('')
    return column

def clean_string(s):
    """Nettoie une chaîne pour l'insertion SQL.
    Renvoie 'Non renseigné' si la valeur est absente ou égale à 'n/a'."""
    if s is None or s.strip() == '' or s.strip().lower() == 'n/a':
        return "Non renseigné"
    return s.replace("'", "''")

def parse_date(date_str):
    """Convertit une chaîne de date en format PostgreSQL valide.
    Retourne None si la date est absente ou invalide."""
    if date_str is None or date_str.strip() == '' or date_str.strip().lower() == 'n/a':
        return None
    # Si la date contient un tiret, on prend la première partie
    if '-' in date_str:
        date_str = date_str.split('-')[0].strip()
    try:
        if '/' in date_str:
            day, month, year = date_str.split('/')
            return f"{year}-{month.zfill(2)}-{day.zfill(2)}"
        else:
            return f"{date_str}-01-01"
    except:
        return None

# Extraction des données depuis le CSV
mariage_id = extract_column('mariages_L3_5K.csv', 0)
mariage_type = extract_column('mariages_L3_5K.csv', 1)
noms_personnes_1 = extract_column('mariages_L3_5K.csv', 2)
prenoms_personnes_1 = extract_column('mariages_L3_5K.csv', 3)
prenoms_peres_personnes_1 = extract_column('mariages_L3_5K.csv', 4)
noms_meres_personnes_1 = extract_column('mariages_L3_5K.csv', 5)
prenoms_meres_personnes_1 = extract_column('mariages_L3_5K.csv', 6)
noms_personnes_2 = extract_column('mariages_L3_5K.csv', 7)
prenoms_personnes_2 = extract_column('mariages_L3_5K.csv', 8)
prenoms_peres_personnes_2 = extract_column('mariages_L3_5K.csv', 9)
noms_meres_personnes_2 = extract_column('mariages_L3_5K.csv', 10)
prenoms_meres_personnes_2 = extract_column('mariages_L3_5K.csv', 11)
les_communes = extract_column('mariages_L3_5K.csv', 12)
les_departements = extract_column('mariages_L3_5K.csv', 13)
les_dates = extract_column('mariages_L3_5K.csv', 14)
les_nums_vues = extract_column('mariages_L3_5K.csv', 15)

with open('Donnees_mariage.sql', 'w', encoding='utf-8') as file:
    # Insertion des départements
    file.write("-- Insertion des départements\n")
    for dept in set(les_departements):
        if dept.isdigit():
            file.write(f'INSERT INTO "Departement" ("id_departement", "nom_departement") '
                       f"VALUES ({dept}, '{clean_string(dept)}') ON CONFLICT DO NOTHING;\n")
    
    # Insertion des communes
    file.write("\n-- Insertion des communes\n")
    communes_vues = set()
    for i, commune in enumerate(les_communes):
        if (commune, les_departements[i]) not in communes_vues and les_departements[i].isdigit():
            file.write(f'INSERT INTO "Commune" ("nom_commune", "id_departement") '
                       f"VALUES ('{clean_string(commune)}', {les_departements[i]});\n")
            communes_vues.add((commune, les_departements[i]))
    
    # Insertion des types d'actes
    file.write("\n-- Insertion des types d'actes\n")
    types_acte = {
        'Mariage': 1,
        'Contrat de mariage': 2,
        'Publication de mariage': 3,
        'Promesse de mariage - fiançailles': 4,
        'Certificat de mariage': 5,
        'Rectification de mariage': 6,
        'Divorce': 7
    }
    for type_name, type_id in types_acte.items():
        file.write(f'INSERT INTO "Type_Acte" ("id_type_acte", "libelle") '
                   f"VALUES ({type_id}, '{clean_string(type_name)}') ON CONFLICT DO NOTHING;\n")
    
    # Insertion des personnes et des actes
    file.write("\n-- Insertion des personnes et actes\n")
    for i in range(len(mariage_id)):
        # Générer des UUID pour chaque personne
        uuid_1 = str(uuid.uuid4())
        uuid_2 = str(uuid.uuid4())
        
        # Insertion systématique de la première personne
        file.write(f'INSERT INTO "Personne" ("id_personne", "nom", "prenom", "prenom_pere", '
                   f'"nom_mere", "prenom_mere") VALUES ('
                   f"'{uuid_1}', "
                   f"'{clean_string(noms_personnes_1[i])}', "
                   f"'{clean_string(prenoms_personnes_1[i])}', "
                   f"'{clean_string(prenoms_peres_personnes_1[i])}', "
                   f"'{clean_string(noms_meres_personnes_1[i])}', "
                   f"'{clean_string(prenoms_meres_personnes_1[i])}');\n")
        
        # Insertion systématique de la deuxième personne
        file.write(f'INSERT INTO "Personne" ("id_personne", "nom", "prenom", "prenom_pere", '
                   f'"nom_mere", "prenom_mere") VALUES ('
                   f"'{uuid_2}', "
                   f"'{clean_string(noms_personnes_2[i])}', "
                   f"'{clean_string(prenoms_personnes_2[i])}', "
                   f"'{clean_string(prenoms_peres_personnes_2[i])}', "
                   f"'{clean_string(noms_meres_personnes_2[i])}', "
                   f"'{clean_string(prenoms_meres_personnes_2[i])}');\n")
        
        # Préparer la date : si invalide, utiliser une valeur par défaut (par exemple "1900-01-01")
        parsed_date = parse_date(les_dates[i])
        date_value = parsed_date if parsed_date is not None else "1900-01-01"
        
        # Insertion de l'acte sans condition (on insère pour chaque ligne)
        file.write(f'INSERT INTO "Acte" ("date_acte", "num_vue", "id_type_acte", '
                   f'"id_commune", "id_personne_A", "id_personne_B") '
                   f"SELECT '{date_value}', '{clean_string(les_nums_vues[i])}', "
                   f"{types_acte.get(mariage_type[i], 1)}, c.id_commune, '{uuid_1}', '{uuid_2}' "
                   f'FROM "Commune" c '
                   f"WHERE c.nom_commune = '{clean_string(les_communes[i])}' "
                   f"AND c.id_departement = {les_departements[i]} LIMIT 1;\n")

print("Created/Modified files during execution:")
print("Donnees_mariage_bonus.sql")
