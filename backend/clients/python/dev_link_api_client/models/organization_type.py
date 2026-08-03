from enum import Enum


class OrganizationType(str, Enum):
    COMMUNITY = "community"
    COMPANY = "company"
    OPEN_SOURCE = "open_source"
    STARTUP = "startup"
    UNIVERSITY = "university"

    def __str__(self) -> str:
        return str(self.value)
