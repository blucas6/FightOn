import socket
import threading
from config import *

class Client:
    def __init__(self, squeue):
        self.host = IP_ADDR
        self.port = PORT_NUMBER
        self.connected = False
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listen_thread = threading.Thread(target=self.listen, daemon=True)
        self.SERVER_QUEUE = squeue

    def start_client(self):
        self.connect()
        self.send("Hello, Server!")

    def connect(self):
        try:
            self.socket.connect((self.host, self.port))
            self.connected = True
            self.listen_thread.start()
        except Exception as e:
            print(f"Client socket error -> {e}")

    def listen(self):
        while self.connected:
            try:
                # Check for incoming data
                data = self.socket.recv(1024).decode()
                if data:
                    # print(f"CLIENT REC: [{data} {len(data)}]")
                    # Process incoming data
                    if data == MSGTYPE.QUIT.value:
                        self.connected = False
                        break
                    self.SERVER_QUEUE.put(data)
            except Exception as e:
                print(f"Client communication error -> {e}")
                self.connected = False
        print('Client is not connected.')

    def send(self, data):
        if self.connected:
            ok = self.socket.send(data.encode())
            if ok == len(data):
                print(f"CLIENT SEND: [{data} {len(data)}/{ok}] OK")
            else:
                print(f"CLIENT SEND: [{data} {len(data)}/{ok}] FAILED")
        else:
            print("CLIENT SEND: Failed not connected!")

    def close(self):
        self.connected = False
        self.socket.close()
