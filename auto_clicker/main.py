import sys
import threading
import time
import pyautogui
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QSpinBox, QLineEdit, QTextEdit
)
from PyQt5.QtCore import Qt
from flask import Flask, request, jsonify
import json

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
        qt_window.receive_command(cmd, value)
    return jsonify({'status': 'ok'})

def run_flask():
    app.run(host='127.0.0.1', port=SERVER_PORT, debug=False, use_reloader=False)

# --- PyQt5 GUI ---
class AutoClickerMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Auto Clicker')
        self.setGeometry(100, 100, 500, 400)

        # Widgets
        self.label = QLabel('Welcome to Auto Clicker!', self)
        self.label.setAlignment(Qt.AlignCenter)

        self.x_input = QSpinBox()
        self.x_input.setRange(0, 10000)
        self.x_input.setPrefix('X: ')
        self.y_input = QSpinBox()
        self.y_input.setRange(0, 10000)
        self.y_input.setPrefix('Y: ')
        self.pick_btn = QPushButton('Pick Position')

        self.interval_input = QSpinBox()
        self.interval_input.setRange(1, 10000)
        self.interval_input.setValue(100)
        self.interval_input.setSuffix(' ms')
        self.interval_input.setPrefix('Interval: ')

        self.count_input = QSpinBox()
        self.count_input.setRange(0, 1000000)
        self.count_input.setValue(0)
        self.count_input.setPrefix('Count: ')
        self.count_input.setToolTip('0 = infinite')

        self.start_btn = QPushButton('Start')
        self.stop_btn = QPushButton('Stop')
        self.stop_btn.setEnabled(False)

        self.status_label = QLabel('Status: Idle')
        self.status_label.setAlignment(Qt.AlignCenter)

        self.last_command_label = QLabel('Last Command:')
        self.last_command_field = QLineEdit()
        self.last_command_field.setReadOnly(True)

        self.component_info_label = QLabel('Selected Component Info:')
        self.component_info_field = QTextEdit()
        self.component_info_field.setReadOnly(True)
        self.component_info_field.setMinimumHeight(80)

        # Layouts
        coord_layout = QHBoxLayout()
        coord_layout.addWidget(self.x_input)
        coord_layout.addWidget(self.y_input)
        coord_layout.addWidget(self.pick_btn)

        interval_layout = QHBoxLayout()
        interval_layout.addWidget(self.interval_input)
        interval_layout.addWidget(self.count_input)

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.start_btn)
        btn_layout.addWidget(self.stop_btn)

        command_layout = QVBoxLayout()
        command_layout.addWidget(self.last_command_label)
        command_layout.addWidget(self.last_command_field)

        component_layout = QVBoxLayout()
        component_layout.addWidget(self.component_info_label)
        component_layout.addWidget(self.component_info_field)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.label)
        main_layout.addLayout(coord_layout)
        main_layout.addLayout(interval_layout)
        main_layout.addLayout(btn_layout)
        main_layout.addWidget(self.status_label)
        main_layout.addLayout(command_layout)
        main_layout.addLayout(component_layout)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # State
        self.clicking = False
        self.click_thread = None
        self.picking_position = False

        # Connect signals
        self.start_btn.clicked.connect(self.start_clicking)
        self.stop_btn.clicked.connect(self.stop_clicking)
        self.pick_btn.clicked.connect(self.pick_position)

    def start_clicking(self):
        if self.clicking:
            return
        x = self.x_input.value()
        y = self.y_input.value()
        interval = self.interval_input.value() / 1000.0  # ms to seconds
        count = self.count_input.value()
        self.clicking = True
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.status_label.setText('Status: Clicking...')
        self.click_thread = threading.Thread(target=self.click_loop, args=(x, y, interval, count), daemon=True)
        self.click_thread.start()

    def stop_clicking(self):
        self.clicking = False
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.status_label.setText('Status: Stopped')

    def click_loop(self, x, y, interval, count):
        clicks_done = 0
        while self.clicking and (count == 0 or clicks_done < count):
            pyautogui.click(x, y)
            clicks_done += 1
            time.sleep(interval)
        self.clicking = False
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.status_label.setText('Status: Idle')

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
            self.start_clicking()
        elif cmd == "stop_click":
            self.stop_clicking()
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

if __name__ == '__main__':
    # Start Flask server in a background thread
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    app_qt = QApplication(sys.argv)
    qt_window = AutoClickerMainWindow()
    qt_window.show()
    sys.exit(app_qt.exec_()) 