import enum

MYPLAYER = 'sprites/music_note_man.png'
FPS = 60

PORT_NUMBER = 7770
IP_ADDR = 'localhost'

class MSGTYPE(enum.Enum):
    HELLO = '#H'            #H[image]
    QUIT = 'Closing Server Request'
    NEWPLAYER = '#N'        #N[image]
    STARTGAME = 'Start Game Request'



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
