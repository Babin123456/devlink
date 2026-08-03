from enum import Enum


class TeamMemberRole(str, Enum):
    LEADER = "leader"
    MEMBER = "member"

    def __str__(self) -> str:
        return str(self.value)
