import requests
import pandas as pd
from datetime import datetime
import os
import io


#Récupère le flux CSV public d'URLhaus contenant les URLs malveillantes récentes , et retourne un DataFrame pandas.

def collecter_urlhaus():

    url = "https://urlhaus.abuse.ch/downloads/csv_recent/"

    print("Téléchargement des données depuis URLhaus...")
    response = requests.get(url)


    # lève une erreur si le téléchargement échoue
    response.raise_for_status()

    # Le fichier CSV d'URLhaus contient des lignes de commentaires (#) à ignorer
    contenu = response.text
    lignes = [l for l in contenu.split("\n") if not l.startswith("#")]
    csv_propre = "\n".join(lignes)

    # Colonnes définies par URLhaus pour ce flux
    colonnes = [
        "id", "dateadded", "url", "url_status", "last_online",
        "threat", "tags", "urlhaus_link", "reporter"
    ]

    df = pd.read_csv(io.StringIO(csv_propre), names=colonnes, quotechar='"')
    return df


def sauvegarder_csv(df, chemin_fichier):

    if os.path.exists(chemin_fichier):
        historique = pd.read_csv(chemin_fichier)
        combine = pd.concat([historique, df]).drop_duplicates(subset="id", keep="last")
    else:
        combine = df

    combine.to_csv(chemin_fichier, index=False)
    print(f"{len(df)} entrées collectées. Total dans l'historique : {len(combine)}")


if __name__ == "__main__":
    horodatage = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"Collecte lancée le {horodatage}")

    donnees = collecter_urlhaus()

    chemin_csv = os.path.join(os.path.dirname(__file__), "urlhaus_historique.csv")
    sauvegarder_csv(donnees, chemin_csv)