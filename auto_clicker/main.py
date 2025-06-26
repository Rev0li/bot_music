import sys
import threading
import time
import pyautogui
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QSpinBox, QLineEdit, QTextEdit, QListWidget, QListWidgetItem, QComboBox, QTabWidget
)
from PyQt5.QtCore import Qt
from flask import Flask, request, jsonify
import json
import requests
from pywinauto import Desktop
import os

# --- Flask server setup ---
SECRET_TOKEN = "changeme123"  # Change this to a strong random string in production
SERVER_PORT = 5000

app = Flask(__name__)
qt_window = None  # Will be set to the main window instance

@app.route('/command', methods=['POST'])
def command():
    data = request.json
    token = data.get('token')
    if token != SECRET_TOKEN:
        return jsonify({'status': 'error', 'message': 'Unauthorized'}), 401
    cmd = data.get('cmd')
    value = data.get('value')
    if qt_window:
        if cmd == 'trigger_save':
            qt_window.trigger_save_as()
        else:
            qt_window.receive_command(cmd, value)
    return jsonify({'status': 'ok'})

@app.route('/event', methods=['POST'])
def event():
    data = request.json
    event_name = data.get('event')
    if qt_window and hasattr(qt_window, '_event_queue'):
        qt_window._event_queue.put(data)
    if qt_window:
        qt_window.handle_event(data)
    return jsonify({'status': 'ok'})

def run_flask():
    app.run(host='127.0.0.1', port=SERVER_PORT, debug=False, use_reloader=False)

# --- PyQt5 GUI ---
class AutoClickerMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Auto Clicker')
        self.setGeometry(100, 100, 700, 700)

        self.tabs = QTabWidget()
        self.tab_loops = QWidget()
        self.tab_fill_save = QWidget()
        self.tabs.addTab(self.tab_loops, 'Boucles')
        self.tabs.addTab(self.tab_fill_save, 'Fill & Save')

        # --- Onglet Boucles ---
        loops_layout = QVBoxLayout()
        self.label = QLabel('Créer et exécuter des séquences de clics (Auto Clicker)', self)
        self.label.setAlignment(Qt.AlignCenter)
        loops_layout.addWidget(self.label)
        self.action_list = QListWidget()
        self.add_action_btn = QPushButton('Ajouter une action')
        self.remove_action_btn = QPushButton('Supprimer l\'action')
        self.add_action_btn.clicked.connect(self.add_action_dialog)
        self.remove_action_btn.clicked.connect(self.remove_selected_action)
        action_btn_layout = QHBoxLayout()
        action_btn_layout.addWidget(self.add_action_btn)
        action_btn_layout.addWidget(self.remove_action_btn)
        action_layout = QVBoxLayout()
        action_layout.addWidget(QLabel('Séquence d\'actions:'))
        action_layout.addWidget(self.action_list)
        action_layout.addLayout(action_btn_layout)
        self.start_loop_btn = QPushButton('Start Loop')
        self.finish_loop_btn = QPushButton('Finish Loop')
        self.start_loop_btn.clicked.connect(self.start_action_sequence)
        self.finish_loop_btn.clicked.connect(self.stop_action_sequence)
        self.finish_loop_btn.setEnabled(False)
        loop_btn_layout = QHBoxLayout()
        loop_btn_layout.addWidget(self.start_loop_btn)
        loop_btn_layout.addWidget(self.finish_loop_btn)
        self.status_label = QLabel('Status: Idle')
        self.status_label.setAlignment(Qt.AlignCenter)
        self.last_command_label = QLabel('Last Command:')
        self.last_command_field = QLineEdit()
        self.last_command_field.setReadOnly(True)
        self.component_info_label = QLabel('Selected Component Info:')
        self.component_info_field = QTextEdit()
        self.component_info_field.setReadOnly(True)
        self.component_info_field.setMinimumHeight(80)
        command_layout = QVBoxLayout()
        command_layout.addWidget(self.last_command_label)
        command_layout.addWidget(self.last_command_field)
        component_layout = QVBoxLayout()
        component_layout.addWidget(self.component_info_label)
        component_layout.addWidget(self.component_info_field)
        loops_layout.addLayout(action_layout)
        loops_layout.addLayout(loop_btn_layout)
        loops_layout.addWidget(self.status_label)
        loops_layout.addLayout(command_layout)
        loops_layout.addLayout(component_layout)
        self.tab_loops.setLayout(loops_layout)

        # --- Onglet Fill & Save ---
        fill_layout = QVBoxLayout()
        fill_label = QLabel('Remplir et sauvegarder automatiquement vos musiques')
        fill_label.setAlignment(Qt.AlignCenter)
        fill_layout.addWidget(fill_label)
        self.base_path_input = QLineEdit('Music/bot/test/')
        self.base_path_input.setPlaceholderText('Chemin de base (ex: Music/bot/test/)')
        self.artiste_input = QLineEdit()
        self.artiste_input.setPlaceholderText('Artiste')
        self.album_input = QLineEdit()
        self.album_input.setPlaceholderText('Album')
        self.song_input = QLineEdit()
        self.song_input.setPlaceholderText('Song Name')
        path_layout = QHBoxLayout()
        path_layout.addWidget(QLabel('Chemin de base:'))
        path_layout.addWidget(self.base_path_input)
        var_layout = QHBoxLayout()
        var_layout.addWidget(QLabel('Artiste:'))
        var_layout.addWidget(self.artiste_input)
        var_layout.addWidget(QLabel('Album:'))
        var_layout.addWidget(self.album_input)
        var_layout.addWidget(QLabel('Song:'))
        var_layout.addWidget(self.song_input)
        fill_layout.addLayout(path_layout)
        fill_layout.addLayout(var_layout)
        self.save_if_active = False
        self.toggle_save_if_btn = QPushButton('Toggle Save If (OFF)')
        self.toggle_save_if_btn.setCheckable(True)
        self.toggle_save_if_btn.clicked.connect(self.toggle_save_if)
        fill_layout.addWidget(self.toggle_save_if_btn)
        self.tab_fill_save.setLayout(fill_layout)

        container = QWidget()
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.tabs)
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        self.action_sequence = []  # List of dicts: {type, ...}
        self.sequence_running = False
        self.sequence_thread = None

    def start_action_sequence(self):
        if self.sequence_running or not self.action_sequence:
            return
        self.sequence_running = True
        self.start_loop_btn.setEnabled(False)
        self.finish_loop_btn.setEnabled(True)
        self.status_label.setText('Status: Running sequence...')
        self.sequence_thread = threading.Thread(target=self.run_action_sequence, daemon=True)
        self.sequence_thread.start()

    def stop_action_sequence(self):
        self.sequence_running = False
        self.start_loop_btn.setEnabled(True)
        self.finish_loop_btn.setEnabled(False)
        self.status_label.setText('Status: Sequence stopped')

    def run_action_sequence(self):
        for idx, action in enumerate(self.action_sequence):
            if not self.sequence_running:
                break
            if isinstance(action, dict) and action.get('type') == 'click':
                x = int(action.get('x', '0'))
                y = int(action.get('y', '0'))
                pyautogui.click(x, y)
                self.status_label.setText(f'Status: Click ({x}, {y})')
            elif isinstance(action, dict) and action.get('type') == 'sleep':
                duration = int(action.get('duration', '1000'))
                self.status_label.setText(f'Status: Sleep {duration} ms')
                time.sleep(duration / 1000.0)
            elif isinstance(action, dict) and action.get('type') == 'extension':
                msg = action.get('message', '')
                self.status_label.setText(f'Status: Extension message: {msg}')
                try:
                    requests.post('http://127.0.0.1:5000/command', json={
                        'token': 'changeme123',
                        'cmd': 'extension',
                        'value': msg
                    })
                except Exception as e:
                    print('Extension message failed:', e)
            elif isinstance(action, dict) and action.get('type') == 'listen':
                event_name = action.get('event_name', 'lastDl')
                self.status_label.setText(f'Status: Waiting for event: {event_name}')
                self.wait_for_event(event_name)
            time.sleep(0.1)
        self.sequence_running = False
        self.start_loop_btn.setEnabled(True)
        self.finish_loop_btn.setEnabled(False)
        self.status_label.setText('Status: Sequence finished')

    def pick_position(self):
        self.status_label.setText('Status: Click anywhere to pick position...')
        self.picking_position = True
        self.hide()
        time.sleep(0.3)  # Give time for the window to hide
        pos = pyautogui.position()
        self.status_label.setText('Status: Move mouse to position and press any key...')
        # pyautogui.alert('Move your mouse to the desired position and press OK.')
        # Instead of alert, print to console and wait for user to press Enter
        print('Move your mouse to the desired position and press Enter in the terminal...')
        input()
        pos = pyautogui.position()
        self.x_input.setValue(pos.x)
        self.y_input.setValue(pos.y)
        self.picking_position = False
        self.show()
        self.status_label.setText('Status: Idle')

    def receive_command(self, cmd, value):
        self.last_command_field.setText(f"{cmd}: {value}")
        if cmd == "start_click":
            self.start_action_sequence()
        elif cmd == "stop_click":
            self.stop_action_sequence()
        elif cmd == "set_link":
            self.status_label.setText(f"Received link: {value}")
        elif cmd == "select_component":
            # Display all component info in a pretty format
            if isinstance(value, dict):
                info = value
            else:
                try:
                    info = json.loads(value)
                except Exception:
                    info = {"raw": str(value)}
            pretty = "\n".join([f"{k}: {v}" for k, v in info.items()])
            self.component_info_field.setPlainText(pretty)
            self.status_label.setText("Component info received!")

    def add_action_dialog(self):
        from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QFormLayout, QInputDialog, QPushButton
        dialog = QDialog(self)
        dialog.setWindowTitle('Ajouter une action')
        layout = QFormLayout(dialog)
        type_combo = QComboBox()
        type_combo.addItems(['click', 'sleep', 'extension', 'listen'])
        layout.addRow('Type:', type_combo)
        param1 = QLineEdit()
        layout.addRow('Paramètre 1:', param1)
        param2 = QLineEdit()
        layout.addRow('Paramètre 2:', param2)
        pick_btn = QPushButton('Pick Position')
        layout.addRow('', pick_btn)
        pick_btn.setEnabled(type_combo.currentText() == 'click')
        def on_type_change():
            pick_btn.setEnabled(type_combo.currentText() == 'click')
        type_combo.currentTextChanged.connect(on_type_change)
        def pick_position_for_dialog():
            self.status_label.setText('Status: Pick position for action...')
            self.hide()
            time.sleep(0.3)
            print('Déplace la souris à la position voulue et appuie sur Entrée dans le terminal...')
            input()
            pos = pyautogui.position()
            param1.setText(str(pos.x))
            param2.setText(str(pos.y))
            self.show()
            self.status_label.setText('Status: Idle')
        pick_btn.clicked.connect(pick_position_for_dialog)
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        layout.addWidget(buttons)
        def accept():
            action_type = type_combo.currentText()
            p1 = param1.text()
            p2 = param2.text()
            action = {'type': action_type}
            if action_type == 'click':
                action['x'] = str(int(p1)) if p1.isdigit() else '0'
                action['y'] = str(int(p2)) if p2.isdigit() else '0'
                text = f"Click ({action['x']}, {action['y']})"
            elif action_type == 'sleep':
                action['duration'] = str(int(p1)) if p1.isdigit() else '1000'
                text = f"Sleep {action['duration']} ms"
            elif action_type == 'extension':
                action['message'] = p1
                text = f"Extension: {p1}"
            elif action_type == 'listen':
                action['event_name'] = p1 if p1 else 'lastDl'
                text = f"Listen for event: {action['event_name']}"
            self.action_sequence.append(action)
            self.action_list.addItem(str(text))
            dialog.accept()
        buttons.accepted.connect(accept)
        buttons.rejected.connect(dialog.reject)
        dialog.exec_()

    def remove_selected_action(self):
        row = self.action_list.currentRow()
        if row >= 0:
            self.action_list.takeItem(row)
            del self.action_sequence[row]

def trigger_save_as(self):
    base_path, artiste, album, song = self.get_song_metadata()
    full_dir = os.path.join(base_path, artiste, album)
    os.makedirs(full_dir, exist_ok=True)
    full_path = os.path.join(full_dir, song)
    self.status_label.setText(f'Attente de la fenêtre Save As...')
    try:
        print(f'[PY] Remplissage Save As avec : {full_path}')
        # --- MODIFICATION ICI ---
        windows = Desktop(backend="uia").windows()
        for w in windows:
            if "Save As" in w.window_text() or "Enregistrer sous" in w.window_text():
                dlg = w
                break
        else:
            print('[PY] Impossible de trouver la fenêtre Save As pour remplir ! (pywinauto)')
            self.status_label.setText('Fallback pyautogui : Fenêtre Save As non trouvée, tentative auto...')
            import time
            import pyautogui
            time.sleep(1)
            pyautogui.write(full_path)
            pyautogui.press('enter')
            print(f'[PY] (pyautogui) Fichier enregistré : {full_path}')
            self.status_label.setText(f'(pyautogui) Fichier enregistré : {full_path}')
            return
        file_edit = dlg.child_window(class_name="Edit")
        file_edit.set_edit_text(full_path)
        save_btn = dlg.child_window(title_re="Enregistrer|Save", control_type="Button")
        save_btn.click()
        print(f'[PY] Fichier enregistré : {full_path}')
        self.status_label.setText(f'Fichier enregistré : {full_path}')
    except Exception as e:
        print('[PY] Erreur Save As :', e)
        self.status_label.setText(f'Erreur Save As : {e}')


    def get_song_metadata(self):
        # Pour l'instant, lit depuis l'UI, mais pourra lire depuis un fichier/variable partagée plus tard
        base_path = self.base_path_input.text().strip()
        artiste = self.artiste_input.text().strip()
        album = self.album_input.text().strip()
        song = self.song_input.text().strip()
        return base_path, artiste, album, song

    def start_save_as_watcher(self):
        def watcher():
            print('[PY] Watcher Save As démarré, attente de la fenêtre...')
            import time
            time.sleep(1)  # Laisse le temps à la fenêtre de s'ouvrir
def watcher():
    print('[PY] Watcher Save As démarré, attente de la fenêtre...')
    import time
    time.sleep(1)
    while True:
        try:
            # --- MODIFICATION ICI AUSSI ---
            windows = Desktop(backend="uia").windows()
            for w in windows:
                print('[PY] Fenêtre détectée:', w.window_text())
                if "Save As" in w.window_text() or "Enregistrer sous" in w.window_text():
                    print('[PY] Fenêtre Save As détectée !')
                    self.trigger_save_as()
                    return
        except Exception as e:
            print('[PY] Erreur dans watcher Save As:', e)
        time.sleep(1)

        threading.Thread(target=watcher, daemon=True).start()

    def toggle_save_if(self):
        self.save_if_active = not self.save_if_active
        if self.save_if_active:
            self.toggle_save_if_btn.setText('Toggle Save If (ON)')
            self.status_label.setText('Status: Save If watcher ON')
            self.start_save_as_watcher()
        else:
            self.toggle_save_if_btn.setText('Toggle Save If (OFF)')
            self.status_label.setText('Status: Save If watcher OFF')

    def wait_for_event(self, event_name):
        # Attend une requête Flask avec le nom d'événement donné
        import queue
        self._event_queue = getattr(self, '_event_queue', queue.Queue())
        try:
            data = self._event_queue.get(timeout=60)  # Timeout 60s
            if data.get('event') == event_name:
                # Remplit les champs avec les infos reçues
                self.base_path_input.setText(data.get('base_path', ''))
                self.artiste_input.setText(data.get('artiste', ''))
                self.album_input.setText(data.get('album', ''))
                self.song_input.setText(data.get('song', ''))
                self.status_label.setText(f'Status: Event {event_name} received and fields updated')
        except Exception:
            self.status_label.setText(f'Status: Event {event_name} not received (timeout)')

    def handle_event(self, data):
        event_name = data.get('event')
        if event_name == 'lastDl':
            print('[PY] Event lastDl reçu:', data)
            self.base_path_input.setText(data.get('base_path', ''))
            self.artiste_input.setText(data.get('artiste', ''))
            self.album_input.setText(data.get('album', ''))
            self.song_input.setText(data.get('song', ''))
            self.status_label.setText('Status: Infos musique reçues (lastDl)')
            if self.save_if_active:
                print('[PY] Surveillance Save As activée, lancement du watcher...')
                self.status_label.setText('Status: Infos reçues, watcher Save As lancé')
                self.start_save_as_watcher()
            else:
                print('[PY] Surveillance Save As désactivée, rien à faire.')
                self.status_label.setText('Status: Infos reçues, watcher Save As désactivé')

if __name__ == '__main__':
    # Start Flask server in a background thread
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    app_qt = QApplication(sys.argv)
    qt_window = AutoClickerMainWindow()
    qt_window.show()
    sys.exit(app_qt.exec_()) 
