import pygame
from sprite import Sprite, Player

class Game:
    def __init__(self):
        self.TILEWIDTH = 64
        self.WIDTH = 10*self.TILEWIDTH
        self.HEIGHT = 8*self.TILEWIDTH
        self.BACKGROUND = (230, 230, 230)
        self.gamerunning = True
        pygame.init()
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.clock = pygame.time.Clock()
        self.PLAYER1 = Player('sprites/fighter.png', 1*self.TILEWIDTH, 1*self.TILEWIDTH)
        self.TILES = pygame.sprite.Group()
        self.MAP = []
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
                    self.TILES.add(Sprite('sprites/brickbopbrick.png', r*self.TILEWIDTH, c*self.TILEWIDTH))

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.gamerunning = False
        keys = pygame.key.get_pressed()
        self.PLAYER1.ControlMovement(keys)
    def collisions(self):
        #player vs ground
        self.PLAYER1.CheckGroundCollision(self.TILES)   

    def main(self):
        while self.gamerunning:
            self.events()
            self.collisions()
            self.PLAYER1.update()

            self.screen.fill(self.BACKGROUND)
            self.PLAYER1.draw(self.screen)
            self.TILES.draw(self.screen)
            pygame.display.flip()

            self.clock.tick(60)