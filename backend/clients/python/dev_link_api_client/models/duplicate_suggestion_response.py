from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.issue_response import IssueResponse


T = TypeVar("T", bound="DuplicateSuggestionResponse")


@_attrs_define
class DuplicateSuggestionResponse:
    """
    Attributes:
        id (UUID):
        source_issue_id (UUID):
        duplicate_issue_id (UUID):
        similarity_score (float):
        created_at (datetime.datetime):
        issue (IssueResponse | None | Unset):
    """

    id: UUID
    source_issue_id: UUID
    duplicate_issue_id: UUID
    similarity_score: float
    created_at: datetime.datetime
    issue: IssueResponse | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.issue_response import IssueResponse

        id = str(self.id)

        source_issue_id = str(self.source_issue_id)

        duplicate_issue_id = str(self.duplicate_issue_id)

        similarity_score = self.similarity_score

        created_at = self.created_at.isoformat()

        issue: dict[str, Any] | None | Unset
        if isinstance(self.issue, Unset):
            issue = UNSET
        elif isinstance(self.issue, IssueResponse):
            issue = self.issue.to_dict()
        else:
            issue = self.issue

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "source_issue_id": source_issue_id,
                "duplicate_issue_id": duplicate_issue_id,
                "similarity_score": similarity_score,
                "created_at": created_at,
            }
        )
        if issue is not UNSET:
            field_dict["issue"] = issue

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.issue_response import IssueResponse

        d = dict(src_dict)
        id = UUID(d.pop("id"))

        source_issue_id = UUID(d.pop("source_issue_id"))

        duplicate_issue_id = UUID(d.pop("duplicate_issue_id"))

        similarity_score = d.pop("similarity_score")

        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))

        def _parse_issue(data: object) -> IssueResponse | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                issue_type_0 = IssueResponse.from_dict(data)

                return issue_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(IssueResponse | None | Unset, data)

        issue = _parse_issue(d.pop("issue", UNSET))

        duplicate_suggestion_response = cls(
            id=id,
            source_issue_id=source_issue_id,
            duplicate_issue_id=duplicate_issue_id,
            similarity_score=similarity_score,
            created_at=created_at,
            issue=issue,
        )

        duplicate_suggestion_response.additional_properties = d
        return duplicate_suggestion_response

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
