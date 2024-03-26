import socket
import threading

# Get the nickname of the client
nickname=input("Choose a nickname: ")
host = socket.gethostbyname(socket.gethostname())
port = 55555

# Create a socket object for the client
client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

# Connect the client to the server
client.connect((host,port))


# Function to receive messages from the server
def client_receive():
    while True:
        try:
            # Receive the message from the server
            message=client.recv(1024).decode('utf-8')
            # If the message is a request for the nickname, send the nickname to the server
            if message=="NICK?":
                client.send(nickname.encode('utf-8'))
            else:
                # print the received message
                print(message)
        except:
            # Handles the error if it occurs
            print("An error occurred!")
            client.close()
            break

# Function to send messages to the server
def client_send():
    while True:
        # Get the message from the client and send it to the server
        message=f"{nickname}: {input('')}"
        # send the message to the server
        client.send(message.encode('utf-8'))


# Create threads for the client to send and receive messages
receive_thread=threading.Thread(target=client_receive)
receive_thread.start()

# Create a thread to run the function for the client with sending messages
send_thread=threading.Thread(target=client_send)
send_thread.start()

