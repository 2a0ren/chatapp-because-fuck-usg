import socket
import tkinter as tk
from tkinter import scrolledtext

# Connect to the server
def connect_to_server():
    ip = entry_ip.get()
    port = 5555  # Default port, can be changed
    try:
        client_socket.connect((ip, port))
        text_area.insert(tk.END, f"Connected to {ip}\n")
        username = entry_username.get()
        client_socket.send(username.encode('utf-8'))  # Send the username to the server
        receive_messages()  # Start receiving messages from the server
    except:
        text_area.insert(tk.END, f"Failed to connect to {ip}\n")

# Send message to the server
def send_message():
    message = message_entry.get()
    if message:
        client_socket.send(message.encode('utf-8'))
        text_area.insert(tk.END, f"You: {message}\n")
        message_entry.delete(0, tk.END)

# Receive messages from the server
def receive_messages():
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            text_area.insert(tk.END, f"{message}\n")
            text_area.yview(tk.END)
        except:
            break

# Create the socket connection
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# GUI setup
root = tk.Tk()
root.title("Multi-User Chat")

# Create a ScrolledText widget for displaying messages
text_area = scrolledtext.ScrolledText(root, width=50, height=15)
text_area.grid(row=0, column=0, columnspan=2)

# IP entry field
entry_ip = tk.Entry(root, width=30)
entry_ip.grid(row=1, column=0, padx=10)

# Username entry field
entry_username = tk.Entry(root, width=30)
entry_username.grid(row=1, column=1, padx=10)

# Connect Button
connect_button = tk.Button(root, text="Connect", command=connect_to_server)
connect_button.grid(row=2, column=0, columnspan=2)

# Message entry field
message_entry = tk.Entry(root, width=40)
message_entry.grid(row=3, column=0)

# Send Button
send_button = tk.Button(root, text="Send", command=send_message)
send_button.grid(row=3, column=1)

root.mainloop()
