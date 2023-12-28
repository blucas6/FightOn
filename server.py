import socket
import threading
import queue
from config import *

class SocketServer:
    def __init__(self):
        self.host = IP_ADDR                                                 # config dictates addr,port
        self.port = PORT_NUMBER
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)     # socket to connect to clients
        self.client_threads = []                                            # list of client threads

    def start(self):
        self.socket.bind((self.host, self.port))
        self.socket.listen(5)
        print(f'Server listening on ({self.host}, {self.port})')
        self.run_server()

    def run_server(self):
        # check for incoming client connections
        try:
            while True:
                client_socket, addr = self.socket.accept()
                print("Server received connection from", addr)
                client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
                client_thread.start()
                self.client_threads.append(client_thread)
        except socket.error as e:
            print(f"Server error: {e}")
        finally:
            self.socket.close()

    def handle_client(self, client_socket):
        # handle client messages in a separate thread
        while True:
            try:
                data = client_socket.recv(1024).decode()
                if not data:
                    print('Server received no data, quitting...')
                    break
                if data == MSGTYPE.QUIT.value:
                    print(f'Server sending [{MSGTYPE.QUIT.value}]')
                    client_socket.send(MSGTYPE.QUIT.value.encode())
                    print('Server received quit request, quitting...')
                    break
                print(f"Server received from client: [{data}]")
                client_socket.send(data.encode())
            except socket.error as e:
                print(f"Server error handling client: {e}")
                break
        client_socket.close()
        print("Server closed client connection.")

    def close(self):
        # Close all client connections
        for thread in self.client_threads:
            if thread.is_alive():
                thread.join()
        self.socket.close()
        print("Server closed.")

if __name__ == "__main__":
    server = SocketServer()
    server.start()
