"""
service_adapter.py - Adaptateur pour connecter les services existants au frontend moderne
"""

import sys
import os
from typing import Optional, Callable, List, Dict, Any
import threading
from pathlib import Path

# Ajouter le chemin vers les modules existants
current_dir = os.path.dirname(__file__)
root_dir = os.path.join(current_dir, '..', '..', '..')
sys.path.insert(0, root_dir)

try:
    from music_organizer.organizer import MusicOrganizer as MusicScanner
    from music_organizer.monitor import DownloadMonitor  
    from music_organizer.process_activator import SimpleAutoSaver
    SERVICES_AVAILABLE = True
    print("Services backend charges avec succes")
except ImportError as e:
    print(f"Services non disponibles: {e}")
    print(f"Chemin recherche: {root_dir}")
    print(f"Contenu du repertoire: {os.listdir(root_dir) if os.path.exists(root_dir) else 'N/A'}")
    MusicScanner = None
    DownloadMonitor = None
    SimpleAutoSaver = None
    SERVICES_AVAILABLE = False

class ServiceAdapter:
    """
    Adaptateur principal pour connecter les services existants au frontend moderne.
    """
    
    def __init__(self, log_callback: Optional[Callable] = None):
        """
        Initialise l'adaptateur de services.
        
        Args:
            log_callback (Callable): Fonction de logging
        """
        self.log_callback = log_callback or print
        
        # Services
        self.scanner = None
        self.monitor = None
        self.auto_saver = None
        
        # État
        self.is_monitoring = False
        self.auto_save_enabled = True
        self.scan_results = []
        
        # Callbacks pour le frontend
        self.on_download_detected = None
        self.on_scan_progress = None
        self.on_scan_complete = None
        self.on_organize_progress = None
        self.on_organize_complete = None
        
        self._initialize_services()
    
    def _initialize_services(self):
        """Initialise les services disponibles."""
        if not SERVICES_AVAILABLE:
            self.log("Services non disponibles - Mode demo")
            return
        
        try:
            # Initialiser l'auto-saver
            if SimpleAutoSaver:
                self.auto_saver = SimpleAutoSaver(log_callback=self.log)
                self.log("AutoSaver initialise")
            
            # Initialiser le monitor
            if DownloadMonitor:
                self.monitor = DownloadMonitor(
                    notification_callback=self._on_download_notification,
                    log_callback=self.log,
                    auto_paste=True,
                    auto_save=self.auto_save_enabled
                )
                self.log("[OK] DownloadMonitor initialisé")
            
        except Exception as e:
            self.log(f"[ERROR] Erreur initialisation services: {e}")
    
    def log(self, message: str):
        """Log un message."""
        if self.log_callback:
            self.log_callback(message)
    
    # === SCANNER SERVICES ===
    
    def scan_folder(self, folder_path: str, progress_callback: Optional[Callable] = None) -> Dict[str, Any]:
        """
        Scanne un dossier de musique.
        
        Args:
            folder_path (str): Chemin du dossier
            progress_callback (Callable): Callback de progression
            
        Returns:
            dict: Résultats du scan
        """
        if not SERVICES_AVAILABLE or not MusicScanner:
            self.log("[WARN] Scanner non disponible")
            return {"success": False, "error": "Scanner non disponible"}
        
        try:
            self.log(f"[SCAN] Scan du dossier: {folder_path}")
            
            # Créer l'organisateur
            self.scanner = MusicScanner(folder_path, log_callback=self.log)
            
            # Scanner les fichiers
            songs = self.scanner.scan()
            
            # Simuler la progression si callback fourni
            if progress_callback:
                total = len(songs)
                for i, song in enumerate(songs):
                    progress_callback(i + 1, total, song.get('filename', 'Unknown'))
                    if self.on_scan_progress:
                        self.on_scan_progress(i + 1, total, song.get('filename', 'Unknown'))
            
            # Analyser les résultats - tous les songs retournés par scan() sont valides
            valid_songs = songs
            ignored_songs = []  # MusicOrganizer ne retourne que les valides
            
            results = {
                "success": True,
                "total": len(songs),
                "valid": len(valid_songs),
                "ignored": len(ignored_songs),
                "songs": songs,
                "valid_songs": valid_songs,
                "ignored_songs": ignored_songs
            }
            
            self.scan_results = results
            
            # Callback de completion
            if self.on_scan_complete:
                self.on_scan_complete(results)
            
            self.log(f"[OK] Scan termine: {len(songs)} fichiers valides")
            
            return results
            
        except Exception as e:
            error_msg = f"Erreur scan: {str(e)}"
            self.log(f"[ERROR] {error_msg}")
            return {"success": False, "error": error_msg}
    
    def organize_songs(self, target_folder: str, progress_callback: Optional[Callable] = None) -> Dict[str, Any]:
        """
        Organise les chansons scannées.
        
        Args:
            target_folder (str): Dossier de destination (ignoré - utilise le dossier de scan)
            progress_callback (Callable): Callback de progression
            
        Returns:
            dict: Résultats de l'organisation
        """
        if not self.scan_results or not self.scan_results.get("valid_songs"):
            return {"success": False, "error": "Aucune chanson a organiser"}
        
        if not self.scanner:
            return {"success": False, "error": "Scanner non initialise"}
        
        try:
            self.log(f"[FOLDER] Organisation en cours...")
            
            valid_songs = self.scan_results["valid_songs"]
            
            # Simuler la progression
            if progress_callback:
                total = len(valid_songs)
                for i, song in enumerate(valid_songs):
                    progress_callback(i + 1, total, song.get('filename', 'Unknown'))
                    if self.on_organize_progress:
                        self.on_organize_progress(i + 1, total, song.get('filename', 'Unknown'))
            
            # Utiliser la méthode organize de MusicOrganizer
            success_count, error_count = self.scanner.organize()
            
            results = {
                "success": True,
                "organized": success_count,
                "errors": error_count,
                "error_details": [] if error_count == 0 else [f"{error_count} erreurs lors de l'organisation"]
            }
            
            # Callback de completion
            if self.on_organize_complete:
                self.on_organize_complete(results)
            
            self.log(f"[OK] Organisation terminee: {success_count} fichiers organises, {error_count} erreurs")
            
            return results
            
        except Exception as e:
            error_msg = f"Erreur organisation: {str(e)}"
            self.log(f"[ERROR] {error_msg}")
            return {"success": False, "error": error_msg}
    
    # === MONITOR SERVICES ===
    
    def start_monitoring(self) -> bool:
        """
        Démarre le monitoring des téléchargements.
        
        Returns:
            bool: True si succès
        """
        if not self.monitor:
            self.log("[WARN] Monitor non disponible")
            return False
        
        try:
            self.monitor.start()
            self.is_monitoring = True
            self.log("[START] Monitoring démarré")
            return True
        except Exception as e:
            self.log(f"[ERROR] Erreur démarrage monitor: {e}")
            return False
    
    def stop_monitoring(self) -> bool:
        """
        Arrête le monitoring des téléchargements.
        
        Returns:
            bool: True si succès
        """
        if not self.monitor:
            return False
        
        try:
            self.monitor.stop()
            self.is_monitoring = False
            self.log("[STOP] Monitoring arrêté")
            return True
        except Exception as e:
            self.log(f"[ERROR] Erreur arrêt monitor: {e}")
            return False
    
    def set_auto_save(self, enabled: bool):
        """
        Active/désactive l'auto-save.
        
        Args:
            enabled (bool): État de l'auto-save
        """
        self.auto_save_enabled = enabled
        if self.monitor:
            self.monitor.auto_save = enabled
        
        status = "activé" if enabled else "désactivé"
        self.log(f"[SAVE] Auto-Save {status}")
    
    def test_paste(self) -> bool:
        """
        Test le collage automatique.
        
        Returns:
            bool: True si succès
        """
        if not self.auto_saver:
            self.log("[WARN] AutoSaver non disponible")
            return False
        
        try:
            self.log("[TARGET] Test de collage...")
            result = self.auto_saver.simple_save(auto_click_save=self.auto_save_enabled)
            
            if result:
                self.log("[OK] Test réussi!")
            else:
                self.log("[ERROR] Test échoué")
            
            return result
        except Exception as e:
            self.log(f"[ERROR] Erreur test: {e}")
            return False
    
    def toggle_debug(self) -> bool:
        """
        Toggle le mode debug du monitor.
        
        Returns:
            bool: Nouvel état du debug
        """
        if not self.monitor:
            return False
        
        try:
            current = getattr(self.monitor, 'debug_mode', False)
            self.monitor.set_debug_mode(not current)
            
            status = "activé" if not current else "désactivé"
            self.log(f"[DEBUG] Mode debug {status}")
            
            return not current
        except Exception as e:
            self.log(f"[ERROR] Erreur toggle debug: {e}")
            return False
    
    # === CALLBACKS INTERNES ===
    
    def _on_download_notification(self, window_title: str):
        """Callback interne pour les notifications de téléchargement."""
        self.log(f"[NOTIFY] Téléchargement détecté: {window_title}")
        
        if self.on_download_detected:
            self.on_download_detected(window_title)
    
    # === GETTERS ===
    
    def get_status(self) -> Dict[str, Any]:
        """
        Récupère le statut des services.
        
        Returns:
            dict: Statut des services
        """
        return {
            "services_available": SERVICES_AVAILABLE,
            "monitoring": self.is_monitoring,
            "auto_save": self.auto_save_enabled,
            "scanner_available": self.scanner is not None,
            "monitor_available": self.monitor is not None,
            "auto_saver_available": self.auto_saver is not None,
            "last_scan_results": self.scan_results
        }

# Instance globale de l'adaptateur
service_adapter = None

def get_service_adapter(log_callback: Optional[Callable] = None) -> ServiceAdapter:
    """
    Récupère l'instance globale de l'adaptateur de services.
    
    Args:
        log_callback (Callable): Fonction de logging
        
    Returns:
        ServiceAdapter: Instance de l'adaptateur
    """
    global service_adapter
    
    if service_adapter is None:
        service_adapter = ServiceAdapter(log_callback=log_callback)
    
    return service_adapter
