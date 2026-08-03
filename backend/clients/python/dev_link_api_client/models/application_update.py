from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.application_status import ApplicationStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="ApplicationUpdate")


@_attrs_define
class ApplicationUpdate:
    """
    Attributes:
        status (ApplicationStatus | None | Unset):
        message (None | str | Unset):
        portfolio_url (None | str | Unset):
        github_url (None | str | Unset):
        resume_url (None | str | Unset):
        review_notes (None | str | Unset):
        shortlisted (bool | None | Unset):
    """

    status: ApplicationStatus | None | Unset = UNSET
    message: None | str | Unset = UNSET
    portfolio_url: None | str | Unset = UNSET
    github_url: None | str | Unset = UNSET
    resume_url: None | str | Unset = UNSET
    review_notes: None | str | Unset = UNSET
    shortlisted: bool | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        status: None | str | Unset
        if isinstance(self.status, Unset):
            status = UNSET
        elif isinstance(self.status, ApplicationStatus):
            status = self.status.value
        else:
            status = self.status

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

        shortlisted: bool | None | Unset
        if isinstance(self.shortlisted, Unset):
            shortlisted = UNSET
        else:
            shortlisted = self.shortlisted

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if status is not UNSET:
            field_dict["status"] = status
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
        if shortlisted is not UNSET:
            field_dict["shortlisted"] = shortlisted

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_status(data: object) -> ApplicationStatus | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                status_type_0 = ApplicationStatus(data)

                return status_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(ApplicationStatus | None | Unset, data)

        status = _parse_status(d.pop("status", UNSET))

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

        def _parse_shortlisted(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | None | Unset, data)

        shortlisted = _parse_shortlisted(d.pop("shortlisted", UNSET))

        application_update = cls(
            status=status,
            message=message,
            portfolio_url=portfolio_url,
            github_url=github_url,
            resume_url=resume_url,
            review_notes=review_notes,
            shortlisted=shortlisted,
        )

        application_update.additional_properties = d
        return application_update

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
