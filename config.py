import enum

PORT_NUMBER = 7770
IP_ADDR = 'localhost'

class MSGTYPE(enum.Enum):
    HELLO = 'Hello Server!'
    QUIT = 'Closing Server Request'