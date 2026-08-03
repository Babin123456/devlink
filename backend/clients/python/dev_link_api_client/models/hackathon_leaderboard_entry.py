from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="HackathonLeaderboardEntry")


@_attrs_define
class HackathonLeaderboardEntry:
    """
    Attributes:
        team_id (str):
        team_name (str):
        rank (int | Unset):  Default: 0.
        submission_title (str | Unset):  Default: ''.
        avg_score (float | Unset):  Default: 0.0.
        judge_count (int | Unset):  Default: 0.
    """

    team_id: str
    team_name: str
    rank: int | Unset = 0
    submission_title: str | Unset = ""
    avg_score: float | Unset = 0.0
    judge_count: int | Unset = 0
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        team_id = self.team_id

        team_name = self.team_name

        rank = self.rank

        submission_title = self.submission_title

        avg_score = self.avg_score

        judge_count = self.judge_count

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "team_id": team_id,
                "team_name": team_name,
            }
        )
        if rank is not UNSET:
            field_dict["rank"] = rank
        if submission_title is not UNSET:
            field_dict["submission_title"] = submission_title
        if avg_score is not UNSET:
            field_dict["avg_score"] = avg_score
        if judge_count is not UNSET:
            field_dict["judge_count"] = judge_count

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        team_id = d.pop("team_id")

        team_name = d.pop("team_name")

        rank = d.pop("rank", UNSET)

        submission_title = d.pop("submission_title", UNSET)

        avg_score = d.pop("avg_score", UNSET)

        judge_count = d.pop("judge_count", UNSET)

        hackathon_leaderboard_entry = cls(
            team_id=team_id,
            team_name=team_name,
            rank=rank,
            submission_title=submission_title,
            avg_score=avg_score,
            judge_count=judge_count,
        )

        hackathon_leaderboard_entry.additional_properties = d
        return hackathon_leaderboard_entry

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
