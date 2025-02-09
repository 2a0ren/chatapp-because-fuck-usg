import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
import socket as sckt

clients = {}
usernames = {}

# Function to get local IP address of the machine
def get_local_ip():
    hostname = sckt.gethostname()
    local_ip = sckt.gethostbyname(hostname)
    return local_ip

# Handle communication with a single client
def handle_client(client_socket, client_address):
    print(f"{client_address} connected")
    
    # Send prompt for username
    client_socket.send("Enter your username:".encode('utf-8'))
    username = client_socket.recv(1024).decode('utf-8')
    usernames[client_socket] = username
    clients[client_socket] = client_address

    # Notify all clients that a new user has connected
    broadcast(f"{username} has joined the chat!", client_socket)

    while True:
        try:
            # Receive messages from the client
            message = client_socket.recv(1024).decode('utf-8')
            if message.lower() == 'exit':
                break
            broadcast(f"{username}: {message}", client_socket)
        except Exception as e:
            print(f"Error: {e}")
            break

    # Remove the client from the dictionary
    del clients[client_socket]
    del usernames[client_socket]
    client_socket.close()

    # Notify all clients that a user has left
    broadcast(f"{username} has left the chat.", client_socket)

# Broadcast message to all clients
def broadcast(message, sender_socket=None):
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message.encode('utf-8'))
            except:
                pass

# Send message from server UI
def send_message_from_ui():
    message = server_message_entry.get()
    if message:
        broadcast(f"Server: {message}")
        server_text_area.insert(tk.END, f"Server: {message}\n")
        server_message_entry.delete(0, tk.END)

# Set up the server
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    port = 8675
    local_ip = get_local_ip()
    
    # Bind to the server's IP and port
    try:
        server.bind((local_ip, port))
        server.listen(5)
        server_ip_label.config(text=f"Server IP: {local_ip}")
        server_port_label.config(text=f"Server Port: {port}")
        server_status_label.config(text=f"Server started on {local_ip}:{port}")
        print(f"Server started on {local_ip}:{port}")
    except Exception as e:
        print(f"Server error: {e}")
        server_status_label.config(text=f"Error starting server: {e}")
        return
    
    while True:
        try:
            client_socket, client_address = server.accept()
            print(f"Connection accepted from {client_address}")
            # Start a new thread to handle the client
            thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
            thread.start()
        except Exception as e:
            print(f"Error while accepting connection: {e}")

# Set up the server UI
server_window = tk.Tk()
server_window.title("Server Chat UI")

# Set the background color and the font style for a more modern look
server_window.configure(bg="#f0f0f0")
font_style = ("Helvetica", 12)

# Add instructions to the server UI
instruction_label = tk.Label(server_window, text="Server is running...\nWaiting for clients to connect.", font=("Arial", 14), bg="#f0f0f0")
instruction_label.grid(row=0, column=0, columnspan=2, pady=10)

server_text_area = scrolledtext.ScrolledText(server_window, width=50, height=15, font=font_style)
server_text_area.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

server_ip_label = tk.Label(server_window, text="Server IP: Not available", font=font_style, bg="#f0f0f0")
server_ip_label.grid(row=2, column=0, padx=10, pady=10)

server_port_label = tk.Label(server_window, text="Server Port: Not available", font=font_style, bg="#f0f0f0")
server_port_label.grid(row=3, column=0, padx=10, pady=10)

server_status_label = tk.Label(server_window, text="Server Status: Waiting...", font=font_style, bg="#f0f0f0")
server_status_label.grid(row=4, column=0, columnspan=2, pady=10)

server_message_entry = tk.Entry(server_window, width=40, font=font_style)
server_message_entry.grid(row=5, column=0, padx=10)

server_send_button = tk.Button(server_window, text="Send", command=send_message_from_ui, font=font_style, bg="#4CAF50", fg="white")
server_send_button.grid(row=5, column=1, padx=10)

# Run the server in a separate thread to not block the UI
server_thread = threading.Thread(target=start_server, daemon=True)
server_thread.start()

server_window.mainloop()
