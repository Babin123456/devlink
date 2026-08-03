from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="VerificationRequestResponse")


@_attrs_define
class VerificationRequestResponse:
    """
    Attributes:
        id (str):
        user_id (str):
        method (str):
        status (str):
        evidence (None | str | Unset):
        reviewed_by (None | str | Unset):
        reviewed_at (datetime.datetime | None | Unset):
        review_notes (None | str | Unset):
    """

    id: str
    user_id: str
    method: str
    status: str
    evidence: None | str | Unset = UNSET
    reviewed_by: None | str | Unset = UNSET
    reviewed_at: datetime.datetime | None | Unset = UNSET
    review_notes: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        user_id = self.user_id

        method = self.method

        status = self.status

        evidence: None | str | Unset
        if isinstance(self.evidence, Unset):
            evidence = UNSET
        else:
            evidence = self.evidence

        reviewed_by: None | str | Unset
        if isinstance(self.reviewed_by, Unset):
            reviewed_by = UNSET
        else:
            reviewed_by = self.reviewed_by

        reviewed_at: None | str | Unset
        if isinstance(self.reviewed_at, Unset):
            reviewed_at = UNSET
        elif isinstance(self.reviewed_at, datetime.datetime):
            reviewed_at = self.reviewed_at.isoformat()
        else:
            reviewed_at = self.reviewed_at

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
                "user_id": user_id,
                "method": method,
                "status": status,
            }
        )
        if evidence is not UNSET:
            field_dict["evidence"] = evidence
        if reviewed_by is not UNSET:
            field_dict["reviewed_by"] = reviewed_by
        if reviewed_at is not UNSET:
            field_dict["reviewed_at"] = reviewed_at
        if review_notes is not UNSET:
            field_dict["review_notes"] = review_notes

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        user_id = d.pop("user_id")

        method = d.pop("method")

        status = d.pop("status")

        def _parse_evidence(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        evidence = _parse_evidence(d.pop("evidence", UNSET))

        def _parse_reviewed_by(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        reviewed_by = _parse_reviewed_by(d.pop("reviewed_by", UNSET))

        def _parse_reviewed_at(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                reviewed_at_type_0 = datetime.datetime.fromisoformat(data)

                return reviewed_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        reviewed_at = _parse_reviewed_at(d.pop("reviewed_at", UNSET))

        def _parse_review_notes(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        review_notes = _parse_review_notes(d.pop("review_notes", UNSET))

        verification_request_response = cls(
            id=id,
            user_id=user_id,
            method=method,
            status=status,
            evidence=evidence,
            reviewed_by=reviewed_by,
            reviewed_at=reviewed_at,
            review_notes=review_notes,
        )

        verification_request_response.additional_properties = d
        return verification_request_response

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
