import pygame
from sprite import Sprite, Player
from client import Client
from event import Event
import queue
from config import *

class Game:
    def __init__(self):
        self.SERVER_QUEUE = queue.Queue()           # Client receives messages and puts them on the queue
        self.CLIENT = Client(self.SERVER_QUEUE)     # Client object, handles messaging the server
        self.CLIENT.start_client()                  # Start the client

        self.BACKGROUND = (230, 230, 230)           # Background color
        self.gState = GameState.WAITING             # Game running checker
        pygame.init()                               # initialize pygame
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))    # Screen object
        self.clock = pygame.time.Clock()                                    # Pygame clock (framerate)
        self.PLAYER_ID = None
        self.PLAYERS = {}
        self.TILES = pygame.sprite.Group()          # Put all game tiles in the sprite group
        self.MAP = []                               # Map array contains all screen tiles
        self.EVENTER = Event(self)                  # Eventer object for all event processing

    def setupMatch(self):
        # fill screen with match tiles and objects
        print('Game: setup')
        for col in range(int(HEIGHT/TILEWIDTH)):
            rows = []
            for row in range(int(WIDTH/TILEWIDTH)):
                rows.append(0)
            self.MAP.append(rows)
        for r in range(int(WIDTH/TILEWIDTH)):
            self.MAP[-2][r] = 1
        for c in range(int(HEIGHT/TILEWIDTH)):
            for r in range(int(WIDTH/TILEWIDTH)):
                if self.MAP[c][r]:
                    self.TILES.add(Sprite('sprites/brickbopbrick.png', r*TILEWIDTH, c*TILEWIDTH))

    def events(self):
        # process input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.gState = GameState.END
        keys = pygame.key.get_pressed()
        self.EVENTER.deal_with_input(keys)

        # check server queue
        if not self.SERVER_QUEUE.empty():
            msg = self.SERVER_QUEUE.get()
            print(f'CLIENT RECEIVED: [{msg}]')
            self.EVENTER.process_event(msg)

    def AddNewPlayer(self, myplayernumber, img):
        self.PLAYER_ID = myplayernumber
        print(img)
        if self.PLAYER_ID == 0:
            myspot = START_SPOT1
            enemyspot = START_SPOT2
            enemyid = 1
        else:
            myspot = START_SPOT2
            enemyspot = START_SPOT1
            enemyid = 0
        self.PLAYERS[self.PLAYER_ID] = Player(self, MYPLAYER, myspot[0], myspot[1]) 
        self.PLAYERS[enemyid] = Player(self, img, enemyspot[0], enemyspot[1])

    def MovePlayer(self, id, movex, movey):
        try:
            print(f'Game: Moving player {id} ({movex}, {movey})')
            self.PLAYERS[id].addSpeed(movex, movey)
        except Exception as e:
            print(f'Game failed to move player -> {e}')


    def main(self):
        # waiting for players
        self.EVENTER.SendEvent(MSGTYPE.HELLO.value)

        while self.gState == GameState.WAITING:
            self.events()
            self.screen.fill(self.BACKGROUND)
            pygame.display.flip()
            self.clock.tick(FPS)
        # start match
        self.setupMatch()
        while self.gState == GameState.RUNNING:
            try:
                self.screen.fill(self.BACKGROUND)
                self.events()
                for id, pobj in self.PLAYERS.items():
                    pobj.update()
                    pobj.draw(self.screen)
                self.TILES.draw(self.screen)
                pygame.display.flip()
                self.clock.tick(FPS)
            except Exception as e:
                print(f'Error during game loop -> {e}')
        print('GAME END')