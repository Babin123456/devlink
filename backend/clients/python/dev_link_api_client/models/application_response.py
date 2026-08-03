from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.application_status import ApplicationStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="ApplicationResponse")


@_attrs_define
class ApplicationResponse:
    """
    Attributes:
        id (UUID):
        applicant_id (UUID):
        project_id (UUID):
        flare_id (UUID):
        status (ApplicationStatus):
        shortlisted (bool):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        message (None | str | Unset):
        portfolio_url (None | str | Unset):
        github_url (None | str | Unset):
        resume_url (None | str | Unset):
        review_notes (None | str | Unset):
    """

    id: UUID
    applicant_id: UUID
    project_id: UUID
    flare_id: UUID
    status: ApplicationStatus
    shortlisted: bool
    created_at: datetime.datetime
    updated_at: datetime.datetime
    message: None | str | Unset = UNSET
    portfolio_url: None | str | Unset = UNSET
    github_url: None | str | Unset = UNSET
    resume_url: None | str | Unset = UNSET
    review_notes: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        applicant_id = str(self.applicant_id)

        project_id = str(self.project_id)

        flare_id = str(self.flare_id)

        status = self.status.value

        shortlisted = self.shortlisted

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

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

        review_notes: None | str | Unset
        if isinstance(self.review_notes, Unset):
            review_notes = UNSET
        else:
            review_notes = self.review_notes

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "applicant_id": applicant_id,
                "project_id": project_id,
                "flare_id": flare_id,
                "status": status,
                "shortlisted": shortlisted,
                "created_at": created_at,
                "updated_at": updated_at,
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
        if review_notes is not UNSET:
            field_dict["review_notes"] = review_notes

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = UUID(d.pop("id"))

        applicant_id = UUID(d.pop("applicant_id"))

        project_id = UUID(d.pop("project_id"))

        flare_id = UUID(d.pop("flare_id"))

        status = ApplicationStatus(d.pop("status"))

        shortlisted = d.pop("shortlisted")

        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))

        updated_at = datetime.datetime.fromisoformat(d.pop("updated_at"))

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

        def _parse_review_notes(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        review_notes = _parse_review_notes(d.pop("review_notes", UNSET))

        application_response = cls(
            id=id,
            applicant_id=applicant_id,
            project_id=project_id,
            flare_id=flare_id,
            status=status,
            shortlisted=shortlisted,
            created_at=created_at,
            updated_at=updated_at,
            message=message,
            portfolio_url=portfolio_url,
            github_url=github_url,
            resume_url=resume_url,
            review_notes=review_notes,
        )

        application_response.additional_properties = d
        return application_response

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
