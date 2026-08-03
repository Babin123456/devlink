from enum import Enum


class FlareStatus(str, Enum):
    CLOSED = "closed"
    OPEN = "open"
    PAUSED = "paused"

    def __str__(self) -> str:
        return str(self.value)
