# server.py
import sys
import socket
import threading
from flask import Flask
from flask_socketio import SocketIO, send
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QTextEdit, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QFont
from pyngrok import ngrok

# ----- Configuration -----
STATIC_NGROK_DOMAIN = "ferret-notable-jaybird.ngrok-free.app"  # Your static ngrok domain
SERVER_PORT = 5000  # Using port 5000

# ----- Flask and SocketIO Setup -----
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

@socketio.on('message')
def handle_message(data):
    # Broadcast the message to all connected clients.
    send(data, broadcast=True)

# ----- PyQt5 GUI for Server -----
class ServerGUI(QWidget):
    def __init__(self, public_url):
        super().__init__()
        self.public_url = public_url
        self.init_ui()
        # Start the Flask server in a separate thread.
        threading.Thread(target=self.run_server, daemon=True).start()

    def init_ui(self):
        # Set Comic Sans as the font for all widgets.
        self.font = QFont("Comic Sans MS", 10)
        self.setFont(self.font)

        self.setWindowTitle("Omega ChatApp - Server")
        self.setGeometry(100, 100, 500, 600)

        # Create layout
        layout = QVBoxLayout()

        # Public URL label
        self.url_label = QLabel(f"Server URL: http://{self.public_url}:{SERVER_PORT}")
        self.url_label.setFont(QFont("Comic Sans MS", 12))
        layout.addWidget(self.url_label)

        # Local IP (informational only)
        self.local_ip_label = QLabel(f"Local IP: {self.get_local_ip()}")
        self.local_ip_label.setFont(QFont("Comic Sans MS", 10))
        layout.addWidget(self.local_ip_label)

        # Chat log area
        self.chat_log = QTextEdit()
        self.chat_log.setReadOnly(True)
        self.chat_log.setFont(self.font)
        layout.addWidget(self.chat_log)

        # Message input and send button in a horizontal layout.
        h_layout = QHBoxLayout()
        self.input_box = QLineEdit()
        self.input_box.setFont(self.font)
        h_layout.addWidget(self.input_box)
        self.send_button = QPushButton("Send")
        self.send_button.setFont(self.font)
        self.send_button.setStyleSheet("background-color: green; color: white;")
        self.send_button.clicked.connect(self.send_server_message)
        h_layout.addWidget(self.send_button)
        layout.addLayout(h_layout)

        # Info label
        self.info_label = QLabel("Clients can connect using the above URL")
        self.info_label.setFont(self.font)
        layout.addWidget(self.info_label)

        self.setLayout(layout)

    def send_server_message(self):
        message = self.input_box.text().strip()
        if message:
            self.input_box.clear()
            data = {'username': 'Server', 'message': message}
            # Use socketio.emit (which does not require a request context)
            socketio.emit('message', data, broadcast=True)
            self.append_message(f"Server: {message}")

    def append_message(self, message):
        self.chat_log.append(message)

    def get_local_ip(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except Exception:
            return "Unknown"

    def run_server(self):
        socketio.run(app, host="0.0.0.0", port=SERVER_PORT, debug=False)

def main():
    # Use the provided static ngrok domain.
    public_url = STATIC_NGROK_DOMAIN
    app_qt = QApplication(sys.argv)
    gui = ServerGUI(public_url)
    gui.show()
    sys.exit(app_qt.exec_())

if __name__ == "__main__":
    main()
