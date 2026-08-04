from enum import Enum


class HackathonStatus(str, Enum):
    CANCELLED = "cancelled"
    COMPLETED = "completed"
    DRAFT = "draft"
    IN_PROGRESS = "in_progress"
    JUDGING = "judging"
    REGISTRATION_OPEN = "registration_open"

    def __str__(self) -> str:
        return str(self.value)
