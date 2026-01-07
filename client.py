import socket
import threading
import pyfiglet
from termcolor import colored
ascii_banner=pyfiglet.figlet_format("Chat Client")
print(colored(ascii_banner,"green"))
print(colored("made by Shivanshu Prajapati","red"))

HOST="127.0.0.1"
PORT=1234

client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect((HOST,PORT))
username=input("Enter your username: ")
client.send(username.encode())
print(colored("🟢 Connected to sever.........\n","green"))
print("Type '/histroy' to see last 10 messages\n")
def recieve():
    while True:
        try:
            message=client.recv(1024).decode()
            print(f"\n{message}")
            
        except:
            print("❌ Connection closed by the server")
            client.close()
            break

def send():
    while True:
        message=input()
        if "exit" in message.lower():
            client.close()
            break
        client.send(message.encode())
recieve_thread=threading.Thread(target=recieve)
recieve_thread.start()
send()






































































