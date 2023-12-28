import pygame
from config import *

class Event:
    def __init__(self, game):
        self.prev_event = None
        self.Game = game

    def process(self, keys_pressed):
        if keys_pressed[pygame.K_q] and keys_pressed != self.prev_event:
            self.SendEvent(MSGTYPE.QUIT.value)
        if keys_pressed[pygame.K_d] and keys_pressed != self.prev_event:
            self.SendEvent(MSGTYPE.HELLO.value)
        if keys_pressed[pygame.K_LEFT] and not keys_pressed[pygame.K_RIGHT]:
            self.Game.PLAYER1.addSpeed(-1, 0)
        if keys_pressed[pygame.K_RIGHT] and not keys_pressed[pygame.K_LEFT]:
            self.Game.PLAYER1.addSpeed(1, 0)
        if keys_pressed[pygame.K_UP]:
            self.Game.PLAYER1.addSpeed(0, 1)
        if keys_pressed[pygame.K_DOWN]:
            self.Game.PLAYER1.addSpeed(0, -1)
        self.prev_event = keys_pressed

    def SendEvent(self, msgtype):
        try:
            self.Game.CLIENT.send(msgtype)
        except Exception as e:
            print(f'CLIENT: Send event failure -> {e}')
