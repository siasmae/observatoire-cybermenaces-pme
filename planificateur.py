import schedule
import time
from datetime import datetime
from collecte import collecter_urlhaus, sauvegarder_csv
import os

def tache_collecte_quotidienne():
    """
    Exécute une collecte complète : téléchargement + sauvegarde dans l'historique.
    C'est exactement ce que fait collecte.py, mais appelé automatiquement.
    """
    horodatage = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n[{horodatage}] Lancement de la collecte planifiée...")

    try:
        donnees = collecter_urlhaus()
        chemin_csv = os.path.join(os.path.dirname(__file__), "urlhaus_historique.csv")
        sauvegarder_csv(donnees, chemin_csv)
    except Exception as e:
        print(f"Erreur pendant la collecte : {e}")


# Planifie l'exécution tous les jours à 09h00
schedule.every().day.at("09:00").do(tache_collecte_quotidienne)
# Pour tester rapidement sans attendre le lendemain, décommentez la ligne suivante :
# schedule.every(1).minutes.do(tache_collecte_quotidienne)

print("Planificateur démarré. En attente de l'heure programmée (09:00)...")
print("Laissez cette fenêtre ouverte pour que la collecte s'exécute automatiquement.")

while True:
    schedule.run_pending()
    time.sleep(30)  # vérifie toutes les 30 secondes s'il est temps de lancer la tâche