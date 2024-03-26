import threading
import socket

# Get the host IP address and specify the port number
host = socket.gethostbyname(socket.gethostname())
port = 55555

# Create a socket object
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the server to the host and port
server.bind((host, port))

# Listen for incoming connections
server.listen()

# Lists to keep track of the clients and their nicknames
clients = []
nicknames=[]


# Function to broadcast messages to all connected clients
def broadcast(message):
    for client in clients:
        client.send(message)

# Function to handle clients' connections
def handle_client(client):
    while True:
        try:
            # Receive the message from the client
            message = client.recv(1024)
            # Broadcast the message to all connected clients
            broadcast(message)
        except:
            # If an error occurs, close the connection with the client
            index=clients.index(client)
            clients.remove(client)
            client.close()
            nickname=nicknames[index]
            broadcast(f"{nickname} left the chat!".encode('utf-8'))
            nicknames.remove(nickname)
            break
# Main function to receive the clients connection
def receive():
    while True:
        print("Server is running and listening ...")
        # Accept the connection with the client
        client,address = server.accept()
        print(f"Connected with {str(address)}")
        # Request and store the nickname of the client
        client.send("NICK?".encode('utf-8'))
        nickname=client.recv(1024).decode('utf-8')
        # Add the nickname and client to the lists
        nicknames.append(nickname)
        clients.append(client)
        print(f"Nickname of the client is {nickname}".encode('utf-8')) 
        # Broadcast the nickname to all connected clients 
        broadcast(f"{nickname} joined the chat!".encode('utf-8'))
        # Send a welcome message to the client
        client.send("Connected to the server".encode('utf-8'))
        # Start the handling thread for the client
        thread=threading.Thread(target=handle_client,args=(client,))
        thread.start()

# Execute the main function
if __name__=="__main__":
    receive()