from enum import Enum


class IssueDifficulty(str, Enum):
    ADVANCED = "advanced"
    BEGINNER = "beginner"
    EXPERT = "expert"
    INTERMEDIATE = "intermediate"

    def __str__(self) -> str:
        return str(self.value)
