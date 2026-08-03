from enum import Enum


class MessageType(str, Enum):
    AI = "ai"
    FILE = "file"
    IMAGE = "image"
    SYSTEM = "system"
    TEXT = "text"

    def __str__(self) -> str:
        return str(self.value)
