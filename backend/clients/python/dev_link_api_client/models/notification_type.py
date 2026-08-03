from enum import Enum


class NotificationType(str, Enum):
    AI = "ai"
    APPLICATION = "application"
    APPLICATION_ACCEPTED = "application_accepted"
    APPLICATION_REJECTED = "application_rejected"
    BUILDER_FLARE = "builder_flare"
    FOLLOW = "follow"
    MENTION = "mention"
    MESSAGE = "message"
    PASSWORD_RESET = "password_reset"
    PROJECT_INVITE = "project_invite"
    PROJECT_UPDATE = "project_update"
    ROLE_CHANGE = "role_change"
    SECURITY_ALERT = "security_alert"
    SYSTEM = "system"
    WELCOME = "welcome"

    def __str__(self) -> str:
        return str(self.value)
