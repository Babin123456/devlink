from enum import Enum


class ActivityType(str, Enum):
    APPLICATION_ACCEPTED = "application_accepted"
    APPLICATION_REJECTED = "application_rejected"
    APPLICATION_SUBMITTED = "application_submitted"
    BUILDER_FLARE_CREATED = "builder_flare_created"
    COMMENT_CREATED = "comment_created"
    DISCUSSION_CREATED = "discussion_created"
    FOLLOWED_USER = "followed_user"
    MESSAGE_SENT = "message_sent"
    ORGANIZATION_CREATED = "organization_created"
    PROFILE_UPDATED = "profile_updated"
    PROJECT_ANNOUNCEMENT = "project_announcement"
    PROJECT_ARCHIVED = "project_archived"
    PROJECT_CREATED = "project_created"
    PROJECT_MILESTONE = "project_milestone"
    PROJECT_UPDATED = "project_updated"
    REPOSITORY_CONNECTED = "repository_connected"
    SYSTEM = "system"
    TEAM_INVITATION = "team_invitation"
    USER_REGISTERED = "user_registered"

    def __str__(self) -> str:
        return str(self.value)
