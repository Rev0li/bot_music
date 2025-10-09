"""
cleanup.py - Nettoyage du dossier temp/

Supprime tous les fichiers JSON et MP3 temporaires.
Utile en cas d'erreur ou de blocage.
"""

import requests
import sys

def cleanup():
    """Nettoie le dossier temp/ via l'API"""
    try:
        print("🧹 Nettoyage du dossier temp/...")
        
        response = requests.post('http://localhost:5000/cleanup')
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Succès: {data['count']} fichier(s) supprimé(s)")
            if data['deleted_files']:
                print("\nFichiers supprimés:")
                for file in data['deleted_files']:
                    print(f"  - {file}")
        else:
            print(f"❌ Erreur: {response.status_code}")
            print(response.text)
            
    except requests.exceptions.ConnectionError:
        print("❌ Erreur: Serveur Python non accessible")
        print("   Lancez d'abord: python app.py")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Erreur: {e}")
        sys.exit(1)

if __name__ == '__main__':
    cleanup()
