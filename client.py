import socket
import threading
import tkinter
import tkinter.scrolledtext
from tkinter import simpledialog

HOST = socket.gethostbyname(socket.gethostname())
PORT = 5566

class Client:
    def __init__(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))
        
        msg = tkinter.Tk()
        msg.withdraw()
        
        
        self.nickname = simpledialog.askstring("Nickname", "Please choose a nickname\t\t\t", parent=msg) #"\t" just to make the window wider
        
        self.nickname = simpledialog.askstring("Nickname", "Please choose a nickname\t\t\t", parent=msg) #"\t" just to make the window wider
     
        self.gui_done = False
        self.running = True
        
        gui_thread = threading.Thread(target=self.gui_loop)
        receive_thread = threading.Thread(target=self.receive)
        
        gui_thread.start()
        receive_thread.start()
        
    def gui_loop(self):
        self.win = tkinter.Tk()
        self.win.configure(bg="lightgray")
        self.win.title(self.nickname)
        
        self.online_users_list = []
        
        self.chat_label = tkinter.Label(self.win, text="Chat:", bg="lightgray")
        self.chat_label.config(font=("Arial", 12))
        self.chat_label.pack(padx=20, pady=5)
        
        self.text_area = tkinter.scrolledtext.ScrolledText(self.win)
        self.text_area.pack(padx=20, pady=5)
        self.text_area.config(state='disabled') #The user can not edit the text area, 
                                                #but also it means that it can not be edited programmly
                                                #so it needs to be enabled first
    
        self.msg_label = tkinter.Label(self.win, text="Message:", bg="lightgray")
        self.msg_label.config(font=("Arial", 12))
        self.msg_label.pack(padx=20, pady=5)
        
        self.input_area = tkinter.Text(self.win, height=3)
        self.input_area.pack(padx=20, pady=5)
        
        self.send_button = tkinter.Button(self.win, text="Send", command=self.write)
        self.win.bind('<Return>',self.handler)
        self.send_button.config(font=("Arial", 12))
        self.send_button.pack(padx=20, pady=5)
        
        self.leave_button = tkinter.Button(self.win, text="Leave", command=self.stop)
        self.leave_button.config(font=("Arial", 12))
        self.leave_button.pack(padx=20, pady=5)
        
        onlineUsersList = tkinter.Listbox(self.win)
        def do_update():
            onlineUsersList.delete(0, 'end')
            counter = 1
            for onlineuser in self.online_users_list:
                onlineUsersList.insert(counter, onlineuser)
                counter = counter + 1
                
                
        def run_every_minute():
            do_update()
            self.win.after(6, run_every_minute)
        onlineUsersList.pack()
        
        
        self.gui_done = True
        
        run_every_minute()
        self.win.protocol("WM_DELETE_WINDOW", self.stop) #What to do when the window is closed
        self.win.mainloop()
        
    def handler(self, e): #To send the input text when enter is pressed
        self.write()
        
        
    def write(self):
        message = f"{self.nickname}: {self.input_area.get('1.0', 'end')}" #Get the whole text from the input area from the beginning to the end
        self.sock.send(message.encode('utf-8'))
        self.input_area.delete('1.0', 'end')
        
        
    
    def stop(self):
        self.running = False
        self.win.destroy()
        self.sock.close()
        exit(0)
        
    def receive(self):
        while self.running:
            try:
                message = self.sock.recv(1024).decode('utf-8')
                if "online_users" in message:
                    self.online_users_list = message.split("online_users")[0].split(' ') #Last split is to convert the string into a list
                elif message == "send file":
                    print("recieving file")
                    data = client.recv(1024)
                    print("creating the file where to save the data")
                    with open("file.txt", 'wb') as f:
                        f.write(data)
                        print("data recieved")
                        break
                elif message == 'NICK':
                    self.sock.send(self.nickname.encode('utf-8'))
                else:
                    if self.gui_done:
                        self.text_area.config(state='normal')
                        self.text_area.insert('end', message)
                        self.text_area.yview('end')
                        self.text_area.config(state='disabled')
                        
            except ConnectionAbortedError:
                break
            except:
                print("Error")
                self.sock.close()
                break
                
                
client = Client(HOST, PORT) 