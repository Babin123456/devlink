from enum import Enum


class BookmarkTargetType(str, Enum):
    FLARE = "flare"
    PROJECT = "project"

    def __str__(self) -> str:
        return str(self.value)
