import socket
import threading
from config import *

class Client:
    def __init__(self, squeue):
        self.host = IP_ADDR                                                         # config dictates addr,port
        self.port = PORT_NUMBER
        self.connected = False                                                      # keep track if client is connected to server
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)             # client socket to server
        self.listen_thread = threading.Thread(target=self.listen, daemon=True)      # listen thread for messages from server
        self.SERVER_QUEUE = squeue                                                  # put messages from server on queue for the client to read

    def start_client(self):
        try:
            # connect to the server
            self.socket.connect((self.host, self.port))
            self.connected = True
            # start the listening thread
            self.listen_thread.start()
        except Exception as e:
            print(f"Client socket error -> {e}")

    def listen(self):
        # listen for messages from server and put them on the server queue
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
        # Send messages to server
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
