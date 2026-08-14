from enum import Enum


class PrivacyVisibility(str, Enum):
    AUTHENTICATED = "authenticated"
    FOLLOWERS = "followers"
    PRIVATE = "private"
    PUBLIC = "public"

    def __str__(self) -> str:
        return str(self.value)
