from enum import Enum

class MessageTypes(Enum):
    TEXT = 1
    AUDIO = 2
    IMAGE = 3
    VIDEO = 4
    GIF = 5
    STICKER = 6
    DOCUMENT = 7
    LOCATION = 8
    CONTACT = 9
    OTHER = 42
