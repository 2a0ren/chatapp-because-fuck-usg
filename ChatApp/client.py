# client.py
import sys
import threading
import socketio
import tkinter as tk
from tkinter import scrolledtext, messagebox

# Default server URL (set to your static ngrok domain)
DEFAULT_SERVER_URL = f"http://ferret-notable-jaybird.ngrok-free.app"
SERVER_PORT = 80  # Must match the server's port

# Create a Socket.IO client instance
sio = socketio.Client()

class ClientGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.server_url = DEFAULT_SERVER_URL
        self.init_ui()
        self.connect_to_server()

    def init_ui(self):
        self.title("Omega ChatApp - Client")
        self.geometry("500x600")
        self.config(bg="#f0f0f0")
        
        # Server URL label and entry
        self.url_label = tk.Label(self, text="Server URL (include http://):", font=("Arial", 12), bg="#f0f0f0")
        self.url_label.pack(pady=10)
        self.url_entry = tk.Entry(self, width=50)
        self.url_entry.pack(pady=5)
        self.url_entry.insert(0, DEFAULT_SERVER_URL)
        
        self.connect_button = tk.Button(self, text="Reconnect", command=self.reconnect, bg="green", fg="white")
        self.connect_button.pack(pady=10)
        
        # Chat log area
        self.chat_log = scrolledtext.ScrolledText(self, width=60, height=20, state="disabled", wrap=tk.WORD)
        self.chat_log.pack(pady=10)
        
        # Message input field
        self.input_box = tk.Entry(self, width=50)
        self.input_box.pack(pady=5)
        
        # Send button
        self.send_button = tk.Button(self, text="Send", command=self.send_message, bg="green", fg="white")
        self.send_button.pack(pady=5)

    def connect_to_server(self):
        self.server_url = self.url_entry.get().strip()
        try:
            sio.connect(self.server_url, transports=["websocket"])
            self.chat_log.config(state="normal")
            self.chat_log.insert(tk.END, f"Connected to server at {self.server_url}\n")
            self.chat_log.config(state="disabled")
        except Exception as e:
            messagebox.showerror("Connection Error", f"Could not connect to server: {e}")

    def reconnect(self):
        sio.disconnect()
        self.connect_to_server()

    def send_message(self):
        message = self.input_box.get().strip()
        if message:
            data = {'username': 'Client', 'message': message}
            sio.emit('message', data)
            self.append_message(f"You: {message}")
            self.input_box.delete(0, tk.END)

    def append_message(self, message):
        self.chat_log.config(state="normal")
        self.chat_log.insert(tk.END, message + "\n")
        self.chat_log.yview(tk.END)
        self.chat_log.config(state="disabled")

@sio.on('message')
def on_message(data):
    username = data.get('username', 'Unknown')
    message = data.get('message', '')
    app_instance.append_message(f"{username}: {message}")

def main():
    global app_instance
    app = tk.Tk()
    app_instance = ClientGUI()
    app_instance.mainloop()

if __name__ == "__main__":
    main()
