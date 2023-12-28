import pygame
from sprite import Sprite, Player
from client import Client
from event import Event
import queue
from config import *

class GameState(enum.Enum):
    RUNNING = 1     # running match
    WAITING = 2     # waiting for players
    END = 3         # end game

class Game:
    def __init__(self):
        self.SERVER_QUEUE = queue.Queue()           # Client receives messages and puts them on the queue
        self.CLIENT = Client(self.SERVER_QUEUE)     # Client object, handles messaging the server
        self.CLIENT.start_client()                  # Start the client
        self.TILEWIDTH = 64                         # Tilewidth for tiles (sq)
        self.WIDTH = 10*self.TILEWIDTH              # Calculate height and width of screen
        self.HEIGHT = 8*self.TILEWIDTH
        self.BACKGROUND = (230, 230, 230)           # Background color
        self.gState = GameState.WAITING             # Game running checker
        pygame.init()                               # initialize pygame
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))    # Screen object
        self.clock = pygame.time.Clock()                                    # Pygame clock (framerate)
        self.PLAYER1 = Player(self, MYPLAYER, 1*self.TILEWIDTH, 1*self.TILEWIDTH) 
        self.PLAYER2 = None
        self.TILES = pygame.sprite.Group()          # Put all game tiles in the sprite group
        self.MAP = []                               # Map array contains all screen tiles
        self.EVENTER = Event(self)                  # Eventer object for all event processing

    def setupMatch(self):
        # fill screen with match tiles and objects
        print('Game: setup')
        for col in range(int(self.HEIGHT/self.TILEWIDTH)):
            rows = []
            for row in range(int(self.WIDTH/self.TILEWIDTH)):
                rows.append(0)
            self.MAP.append(rows)
        for r in range(int(self.WIDTH/self.TILEWIDTH)):
            self.MAP[-2][r] = 1
        for c in range(int(self.HEIGHT/self.TILEWIDTH)):
            for r in range(int(self.WIDTH/self.TILEWIDTH)):
                if self.MAP[c][r]:
                    self.TILES.add(Sprite('sprites/brickbopbrick.png', r*self.TILEWIDTH, c*self.TILEWIDTH))

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

    def AddNewPlayer(self, img):
        print(img)

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
                self.events()
                self.PLAYER1.update()
                self.screen.fill(self.BACKGROUND)
                self.PLAYER1.draw(self.screen)
                self.TILES.draw(self.screen)
                pygame.display.flip()

                self.clock.tick(FPS)
            except Exception as e:
                print(f'Error during game loop -> {e}')
        print('GAME END')