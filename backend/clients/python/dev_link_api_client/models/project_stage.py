from enum import Enum


class ProjectStage(str, Enum):
    BETA = "beta"
    IDEA = "idea"
    MVP = "mvp"
    PRODUCTION = "production"
    VALIDATION = "validation"

    def __str__(self) -> str:
        return str(self.value)
