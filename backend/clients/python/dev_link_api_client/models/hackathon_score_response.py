from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="HackathonScoreResponse")


@_attrs_define
class HackathonScoreResponse:
    """
    Attributes:
        score (int):
        id (UUID):
        submission_id (UUID):
        judge_id (UUID):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        comments (None | str | Unset):
    """

    score: int
    id: UUID
    submission_id: UUID
    judge_id: UUID
    created_at: datetime.datetime
    updated_at: datetime.datetime
    comments: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        score = self.score

        id = str(self.id)

        submission_id = str(self.submission_id)

        judge_id = str(self.judge_id)

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        comments: None | str | Unset
        if isinstance(self.comments, Unset):
            comments = UNSET
        else:
            comments = self.comments

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "score": score,
                "id": id,
                "submission_id": submission_id,
                "judge_id": judge_id,
                "created_at": created_at,
                "updated_at": updated_at,
            }
        )
        if comments is not UNSET:
            field_dict["comments"] = comments

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        score = d.pop("score")

        id = UUID(d.pop("id"))

        submission_id = UUID(d.pop("submission_id"))

        judge_id = UUID(d.pop("judge_id"))

        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))

        updated_at = datetime.datetime.fromisoformat(d.pop("updated_at"))

        def _parse_comments(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        comments = _parse_comments(d.pop("comments", UNSET))

        hackathon_score_response = cls(
            score=score,
            id=id,
            submission_id=submission_id,
            judge_id=judge_id,
            created_at=created_at,
            updated_at=updated_at,
            comments=comments,
        )

        hackathon_score_response.additional_properties = d
        return hackathon_score_response

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
