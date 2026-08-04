from enum import Enum


class RepositoryProvider(str, Enum):
    BITBUCKET = "bitbucket"
    GITHUB = "github"
    GITLAB = "gitlab"

    def __str__(self) -> str:
        return str(self.value)
