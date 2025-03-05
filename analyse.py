import pandas as pd
import matplotlib.pyplot as plt

# Charger les données
df = pd.read_csv("mariages_L3_5k.csv", encoding="utf-8", delimiter=",")

# Renommer les colonnes
df.columns = [
    "id_acte", "Type_Acte", "Nom_A", "Prenom_A", "Prenom_Pere_A", "Nom_Mere_A", "Prenom_Mere_A",
    "Nom_B", "Prenom_B", "Prenom_Pere_B", "Nom_Mere_B", "Prenom_Mere_B",
    "Commune", "Departement", "Date_Acte", "Num_Vue"
]

# Convertir la date en format datetime
df["Date_Acte"] = pd.to_datetime(df["Date_Acte"], dayfirst=True, errors="coerce")

# 🔹 1️⃣ Répartition des types d’actes
plt.figure(figsize=(12, 6))  # Augmenter la taille
type_counts = df["Type_Acte"].value_counts()
bars = plt.bar(type_counts.index, type_counts.values, color="skyblue", edgecolor="black")

# Ajouter les nombres sur les barres
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + 10, int(yval), ha="center", va="bottom", fontsize=10)

plt.title("Répartition des types d'actes", fontsize=14)
plt.xlabel("Type d'acte", fontsize=12)
plt.ylabel("Nombre d'actes", fontsize=12)
plt.xticks(rotation=25, ha="right", fontsize=10)  # Meilleure rotation et alignement
plt.grid(axis="y", linestyle="--", alpha=0.7)
print(df["Type_Acte"].value_counts())
print(df.duplicated().sum()) 

plt.tight_layout()  # Ajustement automatique
plt.show()

# 🔹 2️⃣ Nombre total d’actes par département
plt.figure(figsize=(10, 6))
dept_counts = df["Departement"].value_counts()
bars = plt.bar(dept_counts.index.astype(str), dept_counts.values, color="lightcoral", edgecolor="black")

for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + 10, int(yval), ha="center", va="bottom", fontsize=10)

plt.title("Nombre total d'actes par département", fontsize=14)
plt.xlabel("Département", fontsize=12)
plt.ylabel("Nombre d'actes", fontsize=12)
plt.xticks(fontsize=10)
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.tight_layout()
plt.show()

# 🔹 3️⃣ Top 10 des communes avec le plus d’actes
plt.figure(figsize=(12, 6))
top_communes = df["Commune"].value_counts().head(10)
bars = plt.barh(top_communes.index, top_communes.values, color="lightgreen", edgecolor="black")

for bar in bars:
    xval = bar.get_width()
    plt.text(xval + 5, bar.get_y() + bar.get_height()/2, int(xval), ha="left", va="center", fontsize=10)

plt.title("Top 10 des communes avec le plus d’actes", fontsize=14)
plt.xlabel("Nombre d'actes", fontsize=12)
plt.ylabel("Commune", fontsize=12)
plt.xticks(fontsize=10)
plt.grid(axis="x", linestyle="--", alpha=0.7)
plt.tight_layout()
plt.show()

# 🔹 4️⃣ Vérification des valeurs manquantes
plt.figure(figsize=(12, 6))
missing_values = df.isnull().sum()
missing_values = missing_values[missing_values > 0]  # Ne garder que les colonnes avec des valeurs manquantes
bars = plt.bar(missing_values.index, missing_values.values, color="orange", edgecolor="black")

for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + 10, int(yval), ha="center", va="bottom", fontsize=10)

plt.title("Nombre de valeurs manquantes par colonne", fontsize=14)
plt.xlabel("Colonnes", fontsize=12)
plt.ylabel("Nombre de valeurs manquantes", fontsize=12)
plt.xticks(rotation=25, ha="right", fontsize=10)
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.tight_layout()
plt.show()



