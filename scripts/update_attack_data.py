import os
import requests
import pandas as pd

# URLs des fichiers JSON MITRE ATT&CK
ATTACK_DATA = {
    "enterprise-attack": "https://raw.githubusercontent.com/mitre/cti/master/enterprise-attack/enterprise-attack.json",
    "mobile-attack": "https://raw.githubusercontent.com/mitre/cti/master/mobile-attack/mobile-attack.json",
    "ics-attack": "https://raw.githubusercontent.com/mitre/cti/master/ics-attack/ics-attack.json",
}

# Dossier de sortie des fichiers Excel
OUTPUT_DIR = "data"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def download_json(url):
    """Télécharge un fichier JSON depuis l'URL donnée."""
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    print(f"❌ Erreur de téléchargement : {url}")
    return None

def convert_to_excel(json_data, filename):
    """Convertit les objets STIX de MITRE ATT&CK en fichier Excel."""
    if not json_data:
        return

    objects = json_data.get("objects", [])
    data = []

    for obj in objects:
        if obj.get("type") in ["attack-pattern", "x-mitre-tactic", "course-of-action"]:
            data.append({
                "ID": obj.get("id", ""),
                "Nom": obj.get("name", ""),
                "Type": obj.get("type", ""),
                "Description": obj.get("description", ""),
                "Créé le": obj.get("created", ""),
                "Modifié le": obj.get("modified", ""),
            })

    if data:
        df = pd.DataFrame(data)
        df.to_excel(filename, index=False)
        print(f"✅ Fichier généré : {filename}")

# Télécharger et convertir chaque fichier JSON en Excel
for name, url in ATTACK_DATA.items():
    json_data = download_json(url)
    excel_path = os.path.join(OUTPUT_DIR, f"{name}.xlsx")
    convert_to_excel(json_data, excel_path)
