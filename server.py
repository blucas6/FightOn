import socket
import threading
import queue
from config import *
from event import event_parser

class playerinfo:
    def __init__(self, socket, thread, pnum, image=None):
        self.socket = socket
        self.thread = thread
        self.number = pnum
        self.image = image

class Server:
    def __init__(self):
        self.host = IP_ADDR                                                 # config dictates addr,port
        self.port = PORT_NUMBER
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)     # socket to connect to clients
        self.Players = []

    def start(self):
        self.socket.bind((self.host, self.port))
        self.socket.listen(2)
        print(f'Server listening on ({self.host}, {self.port})')
        self.run_server()

    def run_server(self):
        # check for incoming client connections
        try:
            while True:
                client_socket, addr = self.socket.accept()
                print("Server received connection from", addr)
                playernum = len(self.Players)
                client_thread = threading.Thread(target=self.handle_client, args=(client_socket,playernum))
                self.Players.append(playerinfo(client_socket, client_thread, playernum))
                client_thread.start()
        except socket.error as e:
            print(f"Server error: {e}")
        finally:
            self.socket.close()

    def handle_client(self, client_socket, player_num):
        # handle client messages in a separate thread
        while True:
            try:
                data = client_socket.recv(1024).decode()
                print(f"Server received from client: [{data}]")
                # no data
                if not data:
                    print('Server received no data, quitting...')
                    break
                # quit request
                if data == MSGTYPE.QUIT.value:
                    print(f'Server sending [{MSGTYPE.QUIT.value}]')
                    client_socket.send(MSGTYPE.QUIT.value.encode())
                    print('Server received quit request, quitting...')
                    break
                # process event
                if data[0] == "#":
                    self.process_event(data, player_num)
            except socket.error as e:
                print(f"Server error handling client: {e}")
                break
        client_socket.close()
        print(f"Server closed client connection -> Player {player_num}.")
        self.Players.pop(player_num)

    def process_event(self, data, player_num):
        try:
            args = event_parser(data)
            print(f'Server: parsing args -> {args}')
            if data[1] == "H":
                print('Server: Players ->',self.Players)
                self.Players[player_num].image = args[0]
                print(f'Server: Player{player_num} init with image [{args[0]}]')
                if len(self.Players) == PLAYERSNEEDEDTOSTART:
                    print('Server starting game...')
                    self.StartMatch()
            elif data[1] == "M":
                print(f'Server: Player{args[0]} moves ({args[1]},{args[2]})')
                for p in self.Players:
                    p.socket.send(data.encode())
        except Exception as e:
            print(f'SERVER PARSING ERROR [{data}] -> {e}')

    def StartMatch(self):
        p1 = self.Players[0]
        p2 = self.Players[1]
        p1.socket.send((MSGTYPE.NEWPLAYER.value+'0'+p2.image).encode())
        p2.socket.send((MSGTYPE.NEWPLAYER.value+'1'+p1.image).encode())
        p1.socket.send(MSGTYPE.STARTGAME.value.encode())
        p2.socket.send(MSGTYPE.STARTGAME.value.encode())

    def close(self):
        # Close all client connections
        for thread in self.client_threads:
            if thread.is_alive():
                thread.join()
        self.socket.close()
        print("Server closed.")

if __name__ == "__main__":
    server = Server()
    server.start()
