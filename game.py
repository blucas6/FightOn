import pygame
from sprite import Sprite, Player
from client import Client
from event import Event
import queue

class Game:
    def __init__(self):
        self.SERVER_QUEUE = queue.Queue()
        self.CLIENT = Client(self.SERVER_QUEUE)
        self.CLIENT.start_client()
        self.TILEWIDTH = 64
        self.WIDTH = 10*self.TILEWIDTH
        self.HEIGHT = 8*self.TILEWIDTH
        self.BACKGROUND = (230, 230, 230)
        self.gamerunning = True
        pygame.init()
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.clock = pygame.time.Clock()
        self.PLAYER1 = Player('sprites/music_note_man.png', 1*self.TILEWIDTH, 1*self.TILEWIDTH)
        self.TILES = pygame.sprite.Group()
        self.MAP = []
        self.EVENTER = Event(self)

        for col in range(int(self.HEIGHT/self.TILEWIDTH)):
            rows = []
            for row in range(int(self.WIDTH/self.TILEWIDTH)):
                rows.append(0)
            self.MAP.append(rows)
        for r in range(int(self.WIDTH/self.TILEWIDTH)):
            self.MAP[-2][r] = 1
        print(self.MAP)
        for c in range(int(self.HEIGHT/self.TILEWIDTH)):
            for r in range(int(self.WIDTH/self.TILEWIDTH)):
                if self.MAP[c][r]:
                    self.TILES.add(Sprite('sprites/brick.png', r*self.TILEWIDTH, c*self.TILEWIDTH))

    def events(self):
        # process input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.gamerunning = False
        keys = pygame.key.get_pressed()
        self.EVENTER.process(keys)

        # check server queue
        if not self.SERVER_QUEUE.empty():
            msg = self.SERVER_QUEUE.get()
            print(f'CLIENT RECEIVED: [{msg}]')

    def main(self):
        while self.gamerunning:
            try:
                self.events()
                self.PLAYER1.update()
                self.screen.fill(self.BACKGROUND)
                self.PLAYER1.draw(self.screen)
                self.TILES.draw(self.screen)
                pygame.display.flip()

                self.clock.tick(60)
            except Exception as e:
                print(f'Error during game loop -> {e}')
        print('GAME END')
