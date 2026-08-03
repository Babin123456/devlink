from enum import Enum


class SubmissionStatus(str, Enum):
    ACCEPTED = "accepted"
    DRAFT = "draft"
    IN_REVIEW = "in_review"
    REJECTED = "rejected"
    SUBMITTED = "submitted"

    def __str__(self) -> str:
        return str(self.value)
