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
            print(f"{nicknames[clients.index(client)]} says {message}")
            if "who is online?" in message.decode("utf-8"):
                nicknames_splited = ",".join(nicknames)
                client.send(f'The clients conntected are: {nicknames_splited}\n'.encode('utf-8'))
            elif "send file" in message.decode("utf-8"):
                path = message.decode("utf-8").split("file ")[1]
                path_len = len(path)
                path = path[:path_len - 2] #To remove "\n" at the end of the path
                file = open(path, 'rb')
                data = file.read(1024)
                if data:
                    print("Sending data")
                    broadcast(data)
                    print("Data sent successfully")
                    break
                else:
                    print("failed to send data")
                    break
                    
            elif "to: " in message.decode("utf-8"):
                text = message.decode("utf-8").split("to: ")
                actual_message = text[0].split(":")[1].strip()
                receiver_nickname = text[1].strip()
                sender_nickname = text[0].split(":")[0].strip()
                receiver_index = nicknames.index(receiver_nickname)
                client.send(f"{sender_nickname} TO: ({receiver_nickname}) {actual_message}\n".encode('utf-8'))
                receiver = clients[receiver_index]
                receiver.send(f"(PRIVATE) from {sender_nickname}: {actual_message}\n".encode('utf-8'))
            else :
                broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            nickname = nicknames[index]
            broadcast((f"{nickname} left the conversation :/\n").encode('utf-8'))
            client.close()
            nicknames.remove(nickname)
            broadcast(f"{' '.join(nicknames)} online_users".encode('utf-8')) #To send the updated list of online users and show it in the list box       
            if len(nicknames) == 0:
                print("NO ONE IS CONNECTED :/")
            else:
                print(f'The clients conntected are: {nicknames}')
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
        broadcast(f"{' '.join(nicknames)} online_users".encode('utf-8')) #To send the list of online users and show it in the list box       
        client.send("Connected to the server".encode('utf-8'))
        thread = threading.Thread(target=handle, args=(client,)) #The comma just to make it as a tuple
        thread.start()
        
        
print("Server is running ...")
print("Please <<<<NOTE>>>> use the following commands to enjoy the features of our mini chatter box:\n\n 1-to: (nickname) >>is to send a message privately \n 2-who is online? >>is so you get the list of online clients on the server\n 3-send file with the path wanted >>is to send a specific file\n")
receive()




