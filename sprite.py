import pygame
class Sprite(pygame.sprite.Sprite):
    def __init__(self, image, startx, starty):
        super().__init__()

        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()

        self.rect.x = startx
        self.rect.y = starty

        self.SPEEDX = 3
        self.MOVEMENT = [0, 0]

    def update(self):
        self.rect.move_ip([self.MOVEMENT[0]*self.SPEEDX, 0])
        self.MOVEMENT = [0, 0]

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def addSpeed(self, x, y):
        if x == 1:
            self.MOVEMENT[0] = 1
        if x == -1:
            self.MOVEMENT[0] = -1
        if y == 1:
            self.MOVEMENT[1] = 1
        if y == -1:
            self.MOVEMENT[1] = -1


class Player(Sprite):
    def __init__(self, image, startx, starty):
        super().__init__(image, startx, starty)

