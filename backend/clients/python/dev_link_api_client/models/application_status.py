from enum import Enum


class ApplicationStatus(str, Enum):
    ACCEPTED = "accepted"
    PENDING = "pending"
    REJECTED = "rejected"
    REVIEWING = "reviewing"
    WITHDRAWN = "withdrawn"

    def __str__(self) -> str:
        return str(self.value)
