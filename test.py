import socket
import threading

HOST = socket.gethostbyname(socket.gethostname())
PORT = 5566

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))

server.listen()

clients = []
nicknames = []

def broadcast(message):
    for client in clients:
        client.send(message)


def handle(client):
    while True:
        try:
            message = client.recv(1024)
            file = open("file.txt", 'rb')
            data = file.read(1024)
            print(f"{nicknames[clients.index(client)]} says {message}")
            if "who is online?" in message.decode("utf-8"):
                client.send(f'The clients conntected are: {nicknames}\n'.encode('utf-8'))
            elif "send file" in message.decode("utf-8"):
                if data:
                    print("sending data")
                    broadcast(data)
                    print("data sent successfully")
                    break
                else:
                    print("failed to send data")
                    break
            else :
                broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            nickname = nicknames[index]
            broadcast((f"{nickname} left the conversation :/\n").encode('utf-8'))
            client.close()
            nicknames.remove(nickname)
            if len(nicknames) == 0:
                print("NO ONE IS CONNECTED :/")
            else:
                print(f'The clients conntected are: {nicknames}')
            # broadcast(f'The clients conntected are: {nicknames}'.encode('utf-8'))
            break


def receive():
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}!")
        
        client.send("NICK".encode('utf-8'))
        nickname = client.recv(1024).decode("utf-8")
        
        nicknames.append(nickname)
        clients.append(client)
    
        print(f"Nickname of the client is {nickname}")
        broadcast(f"{nickname} connected to the server!\n".encode('utf-8'))
        nicknames_str = str(nicknames)
        broadcast(f"{nicknames_str} online_users".encode('utf-8'))
        client.send("Connected to the server".encode('utf-8'))
        
        thread = threading.Thread(target=handle, args=(client,)) #The comma just to make it as a tuple
        thread.start()
        
        
print("Server is running ...")
receive()