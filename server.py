import socket
import threading
import pyfiglet
from termcolor import colored
import sqlite3
from datetime import datetime
ascii_banner=pyfiglet.figlet_format("Chat Server")
print(colored(ascii_banner,"green"))
print(colored("made by Shivanshu Prajapati","red"))


HOST="127.0.0.1"
PORT=1234
server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((HOST,PORT))
server.listen()
print("🟢 Server started watting for connection.......")
db=sqlite3.connect('chat.db',check_same_thread=False)
cursor=db.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS messages(
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               username TEXT,
               message TEXT,
               timestamp TEXT
)""")
db.commit()
def save_message(username,message):
    time=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    query="""
          INSERT INTO messages (username,message,timestamp) VALUES (?,?,?)
    """
    cursor.execute(query,(username,message,time))
    db.commit()

def send_history(client):
    query="""
       SELECT username,message,timestamp FROM messages ORDER BY id DESC LIMIT 10
    """
    cursor.execute(query)
    data=cursor.fetchall()
    client.send("\n--------Last 10 messages---------\n".encode())
    for u,m,t in data:
        history=f"[{t}] {u} : {m}\n"
        client.send(history.encode())
    client.send("--------------------------------\n".encode())

clients={}
def handle_client(client):
    while True:
        try:
            message=client.recv(1024).decode()
            if not message:
                break
            if message=="/history":
                send_history(client)
                continue
            username=clients[client]
            save_message(username,message)
            broadcast(f"{username} : {message}",client)
        except:
            print(f"🔴 {clients[client]} disconnected")
            del clients[client]
            client.close()
            break

def broadcast(message,sender):
    for c in clients:
        if c!=sender:
            c.send(message.encode())

while True:
    client,addr=server.accept()
    username=client.recv(1024).decode()
    clients[client]=username
    print(f"🔵 {username} connected from {addr}")
    thread=threading.Thread(target=handle_client,args=(client,))
    thread.start()






    

































