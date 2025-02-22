import os
import requests
import pandas as pd
from stix2 import parse

# URLs des fichiers MITRE ATT&CK JSON
ATTACK_DATA = {
    "enterprise-attack": "https://raw.githubusercontent.com/mitre/cti/master/enterprise-attack/enterprise-attack.json",
    "mobile-attack": "https://raw.githubusercontent.com/mitre/cti/master/mobile-attack/mobile-attack.json",
    "ics-attack": "https://raw.githubusercontent.com/mitre/cti/master/ics-attack/ics-attack.json",
}

# Dossier de sortie
OUTPUT_DIR = "data"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def download_json(url):
    """Télécharge un fichier JSON."""
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    print(f"❌ Erreur de téléchargement : {url}")
    return None

def extract_stix_data(stix_objects):
    """Extrait les données des objets STIX."""
    data = []

    for obj in stix_objects:
        try:
            parsed_obj = parse(obj)  # Parser STIX2
            if parsed_obj.type in ["attack-pattern", "x-mitre-tactic", "course-of-action"]:
                data.append({
                    "ID": parsed_obj.id,
                    "Nom": parsed_obj.name,
                    "Type": parsed_obj.type,
                    "Description": parsed_obj.description if hasattr(parsed_obj, "description") else "",
                    "Créé le": parsed_obj.created,
                    "Modifié le": parsed_obj.modified,
                })
        except Exception as e:
            print(f"⚠️ Erreur de parsing STIX : {e}")

    return data

def convert_to_excel(json_data, filename):
    """Convertit un fichier JSON STIX en Excel."""
    if not json_data:
        return

    stix_objects = json_data.get("objects", [])
    extracted_data = extract_stix_data(stix_objects)

    if extracted_data:
        df = pd.DataFrame(extracted_data)
        df.to_excel(filename, index=False)
        print(f"✅ Fichier généré : {filename}")

# Télécharger et convertir chaque fichier
for name, url in ATTACK_DATA.items():
    json_data = download_json(url)
    excel_path = os.path.join(OUTPUT_DIR, f"{name}.xlsx")
    convert_to_excel(json_data, excel_path)
