from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="MatchedContributor")


@_attrs_define
class MatchedContributor:
    """
    Attributes:
        user_id (UUID):
        username (str):
        full_name (str):
        match_score (float):
        match_reason (str):
        matching_skills (list[str]):
        availability (bool):
        avatar (None | str | Unset):
        headline (None | str | Unset):
    """

    user_id: UUID
    username: str
    full_name: str
    match_score: float
    match_reason: str
    matching_skills: list[str]
    availability: bool
    avatar: None | str | Unset = UNSET
    headline: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        user_id = str(self.user_id)

        username = self.username

        full_name = self.full_name

        match_score = self.match_score

        match_reason = self.match_reason

        matching_skills = self.matching_skills

        availability = self.availability

        avatar: None | str | Unset
        if isinstance(self.avatar, Unset):
            avatar = UNSET
        else:
            avatar = self.avatar

        headline: None | str | Unset
        if isinstance(self.headline, Unset):
            headline = UNSET
        else:
            headline = self.headline

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "user_id": user_id,
                "username": username,
                "full_name": full_name,
                "match_score": match_score,
                "match_reason": match_reason,
                "matching_skills": matching_skills,
                "availability": availability,
            }
        )
        if avatar is not UNSET:
            field_dict["avatar"] = avatar
        if headline is not UNSET:
            field_dict["headline"] = headline

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        user_id = UUID(d.pop("user_id"))

        username = d.pop("username")

        full_name = d.pop("full_name")

        match_score = d.pop("match_score")

        match_reason = d.pop("match_reason")

        matching_skills = cast(list[str], d.pop("matching_skills"))

        availability = d.pop("availability")

        def _parse_avatar(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        avatar = _parse_avatar(d.pop("avatar", UNSET))

        def _parse_headline(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        headline = _parse_headline(d.pop("headline", UNSET))

        matched_contributor = cls(
            user_id=user_id,
            username=username,
            full_name=full_name,
            match_score=match_score,
            match_reason=match_reason,
            matching_skills=matching_skills,
            availability=availability,
            avatar=avatar,
            headline=headline,
        )

        matched_contributor.additional_properties = d
        return matched_contributor

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
