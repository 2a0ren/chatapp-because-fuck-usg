# server.py
import sys
import socket
import threading
from flask import Flask
from flask_socketio import SocketIO, send
import tkinter as tk
from tkinter import scrolledtext, messagebox
from pyngrok import ngrok

# ----- Configuration -----
# Use your static ngrok domain below.
STATIC_NGROK_DOMAIN = "ferret-notable-jaybird.ngrok-free.app"
# The port on which the local server will run (ngrok will tunnel to this port)
SERVER_PORT = 80  

# ----- Flask and SocketIO Setup -----
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

@socketio.on('message')
def handle_message(data):
    # Broadcast received messages to all clients.
    send(data, broadcast=True)

# ----- Tkinter GUI for Server -----
class ServerGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Omega ChatApp - Server")
        self.geometry("500x600")
        self.config(bg="#f0f0f0")
        self.create_widgets()
        # Start the Flask server in a separate thread.
        threading.Thread(target=self.run_server, daemon=True).start()

    def create_widgets(self):
        # Display the static ngrok URL (clients use this to connect)
        self.url_label = tk.Label(self, text=f"Server URL: http://{STATIC_NGROK_DOMAIN}", font=("Arial", 12), bg="#f0f0f0")
        self.url_label.pack(pady=10)
        
        # Optionally, display the local IP (for info only)
        self.local_ip_label = tk.Label(self, text=f"Local IP: {self.get_local_ip()}", font=("Arial", 10), bg="#f0f0f0")
        self.local_ip_label.pack(pady=5)
        
        # Chat log area
        self.chat_log = scrolledtext.ScrolledText(self, width=60, height=20, state="disabled", wrap=tk.WORD)
        self.chat_log.pack(pady=10)
        
        # Input field for server messages
        self.input_box = tk.Entry(self, width=50)
        self.input_box.pack(pady=5)
        
        # Send button
        self.send_button = tk.Button(self, text="Send", command=self.send_server_message, bg="green", fg="white")
        self.send_button.pack(pady=5)
        
        # Info label
        self.info_label = tk.Label(self, text="Clients connect using the above URL", font=("Arial", 10), bg="#f0f0f0")
        self.info_label.pack(pady=5)

    def send_server_message(self):
        message = self.input_box.get().strip()
        if message:
            self.input_box.delete(0, tk.END)
            # Broadcast the message
            data = {'username': 'Server', 'message': message}
            send(data, broadcast=True)
            self.append_message(f"Server: {message}")

    def append_message(self, message):
        self.chat_log.config(state="normal")
        self.chat_log.insert(tk.END, message + "\n")
        self.chat_log.yview(tk.END)
        self.chat_log.config(state="disabled")

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
        # Start the Flask-SocketIO server
        socketio.run(app, host="0.0.0.0", port=SERVER_PORT, debug=False)

def main():
    app_gui = ServerGUI()
    app_gui.mainloop()

if __name__ == "__main__":
    main()
