from enum import Enum


class RegistrationStatus(str, Enum):
    CANCELLED = "cancelled"
    CONFIRMED = "confirmed"
    PENDING = "pending"
    WAITLISTED = "waitlisted"

    def __str__(self) -> str:
        return str(self.value)
