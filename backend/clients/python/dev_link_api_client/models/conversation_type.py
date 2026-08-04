from enum import Enum


class ConversationType(str, Enum):
    AI = "ai"
    DIRECT = "direct"
    GROUP = "group"
    PROJECT = "project"

    def __str__(self) -> str:
        return str(self.value)
