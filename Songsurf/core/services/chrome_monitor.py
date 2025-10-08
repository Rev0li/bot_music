"""
Service de monitoring Chrome - Version simplifiée
"""
import asyncio
import json
import websockets
from threading import Thread
import time

class ChromeMonitor:
    def __init__(self, port=8765, log_callback=None):
        self.port = port
        self.log_callback = log_callback or print
        self._running = False
        self._callbacks = {
            'on_detection': None,
            'on_error': None
        }
        self._server = None
        self._thread = None

    def register_callback(self, event_name, callback):
        """Enregistrer un callback pour les événements"""
        if event_name in self._callbacks:
            self._callbacks[event_name] = callback

    def start(self):
        """Démarrer le service de monitoring"""
        try:
            self._running = True
            self._thread = Thread(target=self._run_server, daemon=True)
            self._thread.start()

            # Attendre un peu pour l'initialisation
            time.sleep(0.1)

            if self._running:
                self.log_callback(f"[OK] Chrome Monitor démarré sur le port {self.port}")
                return True
            else:
                self.log_callback("[ERROR] Échec démarrage Chrome Monitor")
                return False

        except Exception as e:
            self.log_callback(f"[ERROR] Erreur démarrage: {e}")
            return False

    def stop(self):
        """Arrêter le service de monitoring"""
        self._running = False

        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=2.0)

        self.log_callback("[INFO] Chrome Monitor arrêté")
        return True

    def _run_server(self):
        """Fonction principale du serveur WebSocket"""
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

            # Créer le serveur WebSocket
            start_server = websockets.serve(
                self._handle_connection,
                "localhost",
                self.port
            )

            # Démarrer le serveur
            server = loop.run_until_complete(start_server)

            # Garder le serveur actif tant que _running est True
            while self._running:
                loop.run_until_complete(asyncio.sleep(0.1))

            # Fermer le serveur
            server.close()
            loop.run_until_complete(server.wait_closed())

        except Exception as e:
            if self._running:  # Seulement logger si on n'est pas en cours d'arrêt
                self.log_callback(f"[ERROR] Erreur serveur WebSocket: {e}")
        finally:
            try:
                loop.close()
            except:
                pass

    async def _handle_connection(self, websocket, path):
        """Gérer une connexion WebSocket entrante"""
        try:
            async for message in websocket:
                try:
                    # Parser le message JSON
                    data = json.loads(message)

                    # Callback de détection
                    if self._callbacks['on_detection']:
                        try:
                            self._callbacks['on_detection'](data)
                        except Exception as callback_error:
                            self.log_callback(f"[ERROR] Erreur callback détection: {callback_error}")

                except json.JSONDecodeError as json_error:
                    self.log_callback(f"[ERROR] JSON invalide reçu: {json_error}")
                except Exception as msg_error:
                    self.log_callback(f"[ERROR] Erreur traitement message: {msg_error}")

        except websockets.exceptions.ConnectionClosed:
            # Connexion fermée normalement
            pass
        except Exception as conn_error:
            self.log_callback(f"[ERROR] Erreur connexion WebSocket: {conn_error}")

            # Callback d'erreur
            if self._callbacks['on_error']:
                try:
                    self._callbacks['on_error'](str(conn_error))
                except Exception as callback_error:
                    self.log_callback(f"[ERROR] Erreur callback erreur: {callback_error}")

    def is_running(self):
        """Vérifier si le service est en cours d'exécution"""
        return self._running and (self._thread.is_alive() if self._thread else False)
