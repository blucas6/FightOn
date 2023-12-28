import pygame
from config import *

class Event:
    def __init__(self, game):
        self.prev_event = None
        self.Game = game

    def deal_with_input(self, keys_pressed):
        self.Game.PLAYER1.ControlMovement(keys_pressed)
        if keys_pressed[pygame.K_q] and keys_pressed != self.prev_event:
            self.SendEvent(MSGTYPE.QUIT.value)
        if keys_pressed[pygame.K_d] and keys_pressed != self.prev_event:
            self.SendEvent(MSGTYPE.HELLO.value)
        self.prev_event = keys_pressed

    def process_event(self, servermsg):
        try:
            if servermsg[0] == "#":
                if servermsg[1] == "N":
                    self.Game.AddNewPlayer(servermsg[2:])
        except Exception as e:
            print(f'Game Parse Error from Server [{servermsg}] -> {e}')

    def SendEvent(self, msgtype):
        try:
            if msgtype == MSGTYPE.HELLO.value:
                msgtype += MYPLAYER
            self.Game.CLIENT.send(msgtype)
        except Exception as e:
            print(f'CLIENT: Send event failure -> {e}')
