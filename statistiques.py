import pandas as pd
import os

chemin_csv = os.path.join(os.path.dirname(__file__), "urlhaus_historique.csv")
df = pd.read_csv(chemin_csv)

# On extrait uniquement la date (sans l'heure) pour pouvoir regrouper par jour
df['date'] = pd.to_datetime(df['dateadded']).dt.date

print("=" * 55)
print("ÉVOLUTION DU NOMBRE D'ENTRÉES PAR JOUR")
print("=" * 55)
entrees_par_jour = df.groupby('date').size().sort_index()
print(entrees_par_jour)

print("\n" + "=" * 55)
print("STATUT DES URLS PAR JOUR (online vs offline)")
print("=" * 55)
statut_par_jour = df.groupby(['date', 'url_status']).size().unstack(fill_value=0)
print(statut_par_jour)

print("\n" + "=" * 55)
print("TENDANCE DES TAGS DOMINANTS (7 derniers jours vs total)")
print("=" * 55)

# Préparation : un tag par ligne (une entrée peut avoir plusieurs tags)
tags_explodes = df[['date', 'tags']].dropna()
tags_explodes = tags_explodes.assign(tag=tags_explodes['tags'].str.split(',')).explode('tag')
tags_explodes['tag'] = tags_explodes['tag'].str.strip()

derniere_date = df['date'].max()
periode_recente = tags_explodes[tags_explodes['date'] >= (pd.Timestamp(derniere_date) - pd.Timedelta(days=7)).date()]

print("Top 5 tags sur l'ensemble de l'historique :")
print(tags_explodes['tag'].value_counts().head(5))

print("\nTop 5 tags sur les 7 derniers jours :")
print(periode_recente['tag'].value_counts().head(5))

print("\n" + "=" * 55)
print("RÉSUMÉ")
print("=" * 55)
print(f"Période couverte : {df['date'].min()} au {df['date'].max()}")
print(f"Nombre de jours avec au moins une collecte : {df['date'].nunique()}")
print(f"Total d'entrées dans l'historique : {len(df)}")