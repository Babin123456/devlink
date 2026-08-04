from enum import Enum


class IssueStatus(str, Enum):
    CLOSED = "closed"
    DUPLICATE = "duplicate"
    IN_PROGRESS = "in_progress"
    OPEN = "open"

    def __str__(self) -> str:
        return str(self.value)
