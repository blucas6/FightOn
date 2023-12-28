import enum

MYPLAYER = 'sprites/music_note_man.png'
FPS = 60
TILEWIDTH = 64                         # Tilewidth for tiles (sq)
WIDTH = 10*TILEWIDTH              # Calculate height and width of screen
HEIGHT = 8*TILEWIDTH
START_SPOT1 = [10, 10]
START_SPOT2 = [10, 10]

PORT_NUMBER = 7770
IP_ADDR = '10.0.1.6'

class MSGTYPE(enum.Enum):
    HELLO = '#H'            #H[image]
    QUIT = 'Closing Server Request'
    NEWPLAYER = '#N'        #N[image]
    STARTGAME = 'Start Game Request'

class GameState(enum.Enum):
    RUNNING = 1     # running match
    WAITING = 2     # waiting for players
    END = 3         # end game


'''
Server starts
client1 starts -> sends #H[image1] to server
server checks if it has both players -> false
client2 starts -> sends #H[image2] to server
server checks if it has both players -> true
server sends #N[image1] to client2
server sends #N[image2] to client1
server sends STARTGAME request
'''
