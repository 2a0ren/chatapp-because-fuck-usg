import socket
import tkinter as tk
from tkinter import scrolledtext

# Connect to the server
def connect_to_server():
    ip = entry_ip.get()
    port = 8675 # Default port
    try:
        client_socket.connect((ip, port))
        text_area.insert(tk.END, f"Connected to {ip} on port {port}\n")
        username = entry_username.get()
        client_socket.send(username.encode('utf-8'))  # Send the username to the server
        receive_messages()  # Start receiving messages from the server
    except Exception as e:
        text_area.insert(tk.END, f"Failed to connect to {ip} on port {port}: {str(e)}\n")
        text_area.insert(tk.END, "Make sure the server is running and the IP and port are correct.\n")

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
root.title("Chat Client")

# Set the background color and the font style for a modern look
root.configure(bg="#f0f0f0")
font_style = ("Helvetica", 12)

# Add instructions for client UI
instruction_label = tk.Label(root, text="Enter the Server IP and Username to Connect", font=("Arial", 14), bg="#f0f0f0")
instruction_label.grid(row=0, column=0, columnspan=2, pady=10)

# Create a ScrolledText widget for displaying messages
text_area = scrolledtext.ScrolledText(root, width=50, height=15, font=font_style)
text_area.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

# IP entry field
entry_ip_label = tk.Label(root, text="Server IP:", font=font_style, bg="#f0f0f0")
entry_ip_label.grid(row=2, column=0, padx=10)

entry_ip = tk.Entry(root, width=30, font=font_style)
entry_ip.grid(row=2, column=1, padx=10)

# Username entry field
entry_username_label = tk.Label(root, text="Your Username:", font=font_style, bg="#f0f0f0")
entry_username_label.grid(row=3, column=0, padx=10)

entry_username = tk.Entry(root, width=30, font=font_style)
entry_username.grid(row=3, column=1, padx=10)

# Connect Button
connect_button = tk.Button(root, text="Connect", command=connect_to_server, font=font_style, bg="#4CAF50", fg="white")
connect_button.grid(row=4, column=0, columnspan=2, pady=10)

# Message entry field
message_entry = tk.Entry(root, width=40, font=font_style)
message_entry.grid(row=5, column=0)

# Send Button
send_button = tk.Button(root, text="Send", command=send_message, font=font_style, bg="#4CAF50", fg="white")
send_button.grid(row=5, column=1)

root.mainloop()
