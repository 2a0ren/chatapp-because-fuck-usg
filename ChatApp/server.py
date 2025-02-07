import socket
import threading

clients = {}  # Dictionary to store connected clients
usernames = {}  # Dictionary to store usernames for each client

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
        except:
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

# Set up the server
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Default port is 5555, but we can change it easily
    port = 5555
    server.bind(('0.0.0.0', port))  # Bind to all interfaces and specified port
    server.listen(5)
    print(f"Server started on port {port}")

    while True:
        client_socket, client_address = server.accept()
        # Start a new thread to handle the client
        thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        thread.start()

if __name__ == "__main__":
    start_server()
