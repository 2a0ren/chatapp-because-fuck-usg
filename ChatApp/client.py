# client.py
import sys
import threading
import socketio
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QTextEdit, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox
from PyQt5.QtGui import QFont

# Default server URL (using your static ngrok domain)
DEFAULT_SERVER_URL = "http://ferret-notable-jaybird.ngrok-free.app"
SERVER_PORT = 5000  # Must match the server's port

# Create a Socket.IO client instance
sio = socketio.Client()

class ClientGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.server_url = DEFAULT_SERVER_URL
        self.init_ui()
        threading.Thread(target=self.connect_to_server, daemon=True).start()

    def init_ui(self):
        self.font = QFont("Comic Sans MS", 10)
        self.setFont(self.font)
        self.setWindowTitle("Omega ChatApp - Client")
        self.setGeometry(100, 100, 500, 600)

        layout = QVBoxLayout()

        # Server URL entry
        self.url_label = QLabel("Server URL (include http://):")
        self.url_label.setFont(QFont("Comic Sans MS", 12))
        layout.addWidget(self.url_label)
        self.url_entry = QLineEdit()
        self.url_entry.setFont(self.font)
        self.url_entry.setText(DEFAULT_SERVER_URL)
        layout.addWidget(self.url_entry)

        self.connect_button = QPushButton("Reconnect")
        self.connect_button.setFont(self.font)
        self.connect_button.setStyleSheet("background-color: green; color: white;")
        self.connect_button.clicked.connect(self.reconnect)
        layout.addWidget(self.connect_button)

        # Chat log area
        self.chat_log = QTextEdit()
        self.chat_log.setReadOnly(True)
        self.chat_log.setFont(self.font)
        layout.addWidget(self.chat_log)

        # Message input and send button
        h_layout = QHBoxLayout()
        self.input_box = QLineEdit()
        self.input_box.setFont(self.font)
        h_layout.addWidget(self.input_box)
        self.send_button = QPushButton("Send")
        self.send_button.setFont(self.font)
        self.send_button.setStyleSheet("background-color: green; color: white;")
        self.send_button.clicked.connect(self.send_message)
        h_layout.addWidget(self.send_button)
        layout.addLayout(h_layout)

        self.setLayout(layout)

    def connect_to_server(self):
        self.server_url = self.url_entry.text().strip()
        try:
            sio.connect(self.server_url, transports=["websocket"])
            self.append_message(f"Connected to server at {self.server_url}")
        except Exception as e:
            self.append_message(f"Connection error: {e}")

    def reconnect(self):
        sio.disconnect()
        self.connect_to_server()

    def send_message(self):
        message = self.input_box.text().strip()
        if message:
            data = {'username': 'Client', 'message': message}
            sio.emit('message', data)
            self.append_message(f"You: {message}")
            self.input_box.clear()

    def append_message(self, message):
        self.chat_log.append(message)

@sio.on('message')
def on_message(data):
    username = data.get('username', 'Unknown')
    message = data.get('message', '')
    app_instance.append_message(f"{username}: {message}")

def main():
    global app_instance
    qt_app = QApplication(sys.argv)
    app_instance = ClientGUI()
    app_instance.show()
    sys.exit(qt_app.exec_())

if __name__ == "__main__":
    main()
