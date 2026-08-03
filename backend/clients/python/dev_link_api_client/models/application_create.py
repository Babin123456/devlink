from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ApplicationCreate")


@_attrs_define
class ApplicationCreate:
    """
    Attributes:
        project_id (UUID):
        flare_id (UUID):
        message (None | str | Unset):
        portfolio_url (None | str | Unset):
        github_url (None | str | Unset):
        resume_url (None | str | Unset):
    """

    project_id: UUID
    flare_id: UUID
    message: None | str | Unset = UNSET
    portfolio_url: None | str | Unset = UNSET
    github_url: None | str | Unset = UNSET
    resume_url: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        project_id = str(self.project_id)

        flare_id = str(self.flare_id)

        message: None | str | Unset
        if isinstance(self.message, Unset):
            message = UNSET
        else:
            message = self.message

        portfolio_url: None | str | Unset
        if isinstance(self.portfolio_url, Unset):
            portfolio_url = UNSET
        else:
            portfolio_url = self.portfolio_url

        github_url: None | str | Unset
        if isinstance(self.github_url, Unset):
            github_url = UNSET
        else:
            github_url = self.github_url

        resume_url: None | str | Unset
        if isinstance(self.resume_url, Unset):
            resume_url = UNSET
        else:
            resume_url = self.resume_url

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "project_id": project_id,
                "flare_id": flare_id,
            }
        )
        if message is not UNSET:
            field_dict["message"] = message
        if portfolio_url is not UNSET:
            field_dict["portfolio_url"] = portfolio_url
        if github_url is not UNSET:
            field_dict["github_url"] = github_url
        if resume_url is not UNSET:
            field_dict["resume_url"] = resume_url

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        project_id = UUID(d.pop("project_id"))

        flare_id = UUID(d.pop("flare_id"))

        def _parse_message(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        message = _parse_message(d.pop("message", UNSET))

        def _parse_portfolio_url(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        portfolio_url = _parse_portfolio_url(d.pop("portfolio_url", UNSET))

        def _parse_github_url(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        github_url = _parse_github_url(d.pop("github_url", UNSET))

        def _parse_resume_url(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        resume_url = _parse_resume_url(d.pop("resume_url", UNSET))

        application_create = cls(
            project_id=project_id,
            flare_id=flare_id,
            message=message,
            portfolio_url=portfolio_url,
            github_url=github_url,
            resume_url=resume_url,
        )

        application_create.additional_properties = d
        return application_create

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
