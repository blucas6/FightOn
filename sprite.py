import pygame
class Sprite(pygame.sprite.Sprite):
    def __init__(self, image, startx, starty):
        super().__init__()

        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()

        self.rect.x = startx
        self.rect.y = starty

        self.SPEEDX = 3
        self.SPEEDY = 10
        self.VelocityY = 0
        self.startGrav = .5
        self.gravityAmt = .5
        self.isJumping = False
        self.onGround = False
        self.MOVEMENT = [0, 0]

    def update(self):
        self.collisions()
        self.rect.move_ip([self.MOVEMENT[0] * self.SPEEDX,  self.VelocityY])
        self.MOVEMENT = [0, 0]
        #render gravity every frame
        self.gravity()

    def collisions(self):
        pass

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def addSpeed(self, x, y):
        #jumping
        #self.MOVEMENT[1] = 1
        self.VelocityY += y
        #left and right movement
        if x == 1:
            self.MOVEMENT[0] = 1
        elif x == -1:
            self.MOVEMENT[0] = -1
        
    def gravity(self):
        self.addSpeed(0,self.gravityAmt)



class Player(Sprite):
    def __init__(self, game, image, startx, starty):
        self.Game = game    # reference to game object
        super().__init__(image, startx, starty)


    def ControlMovement(self, keys):
        if keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
            self.addSpeed(-1, 0)
        if keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]:
            self.addSpeed(1, 0)
        if keys[pygame.K_UP] and self.onGround and not self.isJumping:
            self.addSpeed(0, -self.SPEEDY)
            self.isJumping = True

    def collisions(self):
        #player vs ground
        if pygame.sprite.spritecollide(self,self.Game.TILES,False):
            for ground in self.Game.TILES:
                if self.rect.colliderect(ground.rect):
                    if (abs(self.rect.bottom - ground.rect.top) > 1):
                        self.rect.bottom = ground.rect.top
            self.onGround = True
            self.gravityAmt = 0
            if (not self.isJumping):
                self.VelocityY = 0
           
        else:
            self.gravityAmt = self.startGrav
            self.onGround = False
            if (self.VelocityY > 0):
                self.isJumping = False

