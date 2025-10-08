#!/usr/bin/env python3
"""
Test rapide de l'organisation via le service adapter.
"""

import sys
import os

# Ajouter le chemin vers les modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_scan_and_organize():
    """Test le scan et l'organisation."""
    print("=== Test Scan et Organisation ===")
    
    try:
        from core.services.service_adapter import get_service_adapter
        
        def log_callback(msg):
            print(f"[LOG] {msg}")
        
        # Créer l'adaptateur
        adapter = get_service_adapter(log_callback=log_callback)
        
        # Vérifier le statut
        status = adapter.get_status()
        print(f"Services disponibles: {status['services_available']}")
        
        if not status['services_available']:
            print("Services non disponibles - arrêt du test")
            return False
        
        # Demander le dossier à scanner
        folder = input("Entrez le chemin du dossier à scanner (ou Entrée pour ignorer): ").strip()
        
        if not folder:
            print("Aucun dossier spécifié - test ignoré")
            return True
        
        if not os.path.exists(folder):
            print(f"Dossier inexistant: {folder}")
            return False
        
        print(f"\n--- Scan du dossier: {folder} ---")
        
        # Scanner
        def progress_callback(current, total, filename):
            print(f"Scan {current}/{total}: {filename[:50]}...")
        
        scan_result = adapter.scan_folder(folder, progress_callback=progress_callback)
        
        if not scan_result["success"]:
            print(f"Erreur scan: {scan_result.get('error', 'Erreur inconnue')}")
            return False
        
        print(f"\nRésultats scan:")
        print(f"- Total: {scan_result['total']}")
        print(f"- Valides: {scan_result['valid']}")
        print(f"- Ignorés: {scan_result['ignored']}")
        
        if scan_result['valid'] == 0:
            print("Aucune chanson valide trouvée")
            return True
        
        # Demander confirmation pour l'organisation
        confirm = input(f"\nOrganiser {scan_result['valid']} chansons ? (o/N): ").strip().lower()
        
        if confirm != 'o':
            print("Organisation annulée")
            return True
        
        print("\n--- Organisation ---")
        
        # Organiser
        def organize_progress_callback(current, total, filename):
            print(f"Organisation {current}/{total}: {filename[:50]}...")
        
        organize_result = adapter.organize_songs(folder, progress_callback=organize_progress_callback)
        
        if not organize_result["success"]:
            print(f"Erreur organisation: {organize_result.get('error', 'Erreur inconnue')}")
            return False
        
        print(f"\nRésultats organisation:")
        print(f"- Organisées: {organize_result['organized']}")
        print(f"- Erreurs: {organize_result['errors']}")
        
        if organize_result['errors'] > 0:
            print("Détails erreurs:")
            for error in organize_result.get('error_details', []):
                print(f"  - {error}")
        
        print("\n[OK] Test terminé avec succès!")
        return True
        
    except Exception as e:
        print(f"[ERROR] Erreur test: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Test principal."""
    print("Test d'Organisation - Service Adapter")
    print("=" * 50)
    
    result = test_scan_and_organize()
    
    print("\n" + "=" * 50)
    if result:
        print("[SUCCESS] Test réussi!")
    else:
        print("[FAILED] Test échoué!")
    
    print("\nPour utiliser l'interface complète:")
    print("python app_modern.py")

if __name__ == "__main__":
    main()
