import pandas as pd
import os

# Chemin vers le fichier CSV (dans le dossier data/)
chemin_csv = os.path.join(os.path.dirname(__file__), "data", "urlhaus_historique.csv")

df = pd.read_csv(chemin_csv)

print("=" * 50)
print("APERÇU GÉNÉRAL")
print("=" * 50)
print(f"Nombre total d'entrées : {len(df)}")
print(f"Colonnes disponibles : {list(df.columns)}")

print("\n" + "=" * 50)
print("PÉRIODE COUVERTE")
print("=" * 50)
print(f"Date la plus ancienne : {df['dateadded'].min()}")
print(f"Date la plus récente : {df['dateadded'].max()}")

print("\n" + "=" * 50)
print("RÉPARTITION PAR TYPE DE MENACE")
print("=" * 50)
print(df['threat'].value_counts())

print("\n" + "=" * 50)
print("RÉPARTITION PAR STATUT")
print("=" * 50)
print(df['url_status'].value_counts())

print("\n" + "=" * 50)
print("QUELQUES EXEMPLES D'URLS")
print("=" * 50)
print(df[['dateadded', 'url', 'threat']].head(5).to_string(index=False))

print("\n" + "=" * 50)
print("TOP 10 DES TAGS LES PLUS FRÉQUENTS")
print("=" * 50)
# Les tags sont séparés par des virgules dans une seule cellule, il faut les exploser
tags_series = df['tags'].dropna().str.split(',').explode().str.strip()
print(tags_series.value_counts().head(10))