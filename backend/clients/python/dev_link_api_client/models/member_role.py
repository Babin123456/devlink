from enum import Enum


class MemberRole(str, Enum):
    ADMIN = "admin"
    CONTRIBUTOR = "contributor"
    CO_OWNER = "co_owner"
    MAINTAINER = "maintainer"
    MEMBER = "member"
    OWNER = "owner"
    REVIEWER = "reviewer"
    VIEWER = "viewer"

    def __str__(self) -> str:
        return str(self.value)
