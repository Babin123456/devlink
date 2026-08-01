from pydantic import BaseModel, Field
from typing import Optional, List


class OAuthProviderItem(BaseModel):
    provider: str
    is_linked: bool
    provider_user_id: Optional[str] = None


class OAuthProvidersListResponse(BaseModel):
    has_password: bool
    linked_count: int
    providers: List[OAuthProviderItem]


class LinkOAuthAccountRequest(BaseModel):
    provider: str = Field(
        ..., description="OAuth provider: github, google, gitlab, linkedin"
    )
    provider_user_id: str = Field(
        ..., min_length=1, description="External user ID from provider"
    )


class UnlinkOAuthAccountRequest(BaseModel):
    provider: str = Field(
        ..., description="OAuth provider: github, google, gitlab, linkedin"
    )
