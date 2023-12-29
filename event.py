import pygame
from config import *

def event_parser(data):
    try:
        if data[0] == "#":
            if data[1] == "N":
                return [data[2], data[3:]]
            elif data[1] == "H":
                return [data[2:]]
            elif data[1] == "M":
                id = int(data[2])
                movex = int(data[4])
                movey = int(data[6])
                if data[3] == '-':
                    movex *= -1
                if data[5] == '-':
                    movey *= -1
                return [id, movex, movey]
        else:
            return []
    except Exception as e:
        print(f'PARSING ERROR -> {e}')
        return []
    
class Event:
    def __init__(self, game):
        self.prev_event = None
        self.Game = game

    def deal_with_input(self, keys_pressed):
        if self.Game.gState == GameState.RUNNING:
            self.Game.PLAYERS[self.Game.PLAYER_ID].ControlMovement(keys_pressed)
        if keys_pressed[pygame.K_q] and keys_pressed != self.prev_event:
            self.SendEvent(MSGTYPE.QUIT.value)
        if keys_pressed[pygame.K_d] and keys_pressed != self.prev_event:
            self.SendEvent(MSGTYPE.HELLO.value)
        self.prev_event = keys_pressed

    def process_event(self, servermsg):
        try:
            args = event_parser(servermsg)
            print(f'Client parsed args -> {args}')
            if servermsg[1] == "N":
                self.Game.AddNewPlayer(args[0], args[1])
            elif servermsg == MSGTYPE.STARTGAME.value:
                self.Game.gState = GameState.RUNNING
            elif servermsg[1] == "M":
                self.Game.MovePlayer(args[0], args[1], args[2])
        except Exception as e:
            print(f'Game Parse Error from Server [{servermsg}] -> {e}')

    def SendEvent(self, msgtype):
        try:
            if msgtype == MSGTYPE.HELLO.value:
                msgtype += MYPLAYER
            self.Game.CLIENT.send(msgtype)
        except Exception as e:
            print(f'CLIENT: Send event failure -> {e}')
