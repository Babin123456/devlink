from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.score_breakdown import ScoreBreakdown


T = TypeVar("T", bound="RecommendedBuilder")


@_attrs_define
class RecommendedBuilder:
    """A single builder recommendation entry.

    Attributes:
        user_id (UUID):
        username (str):
        first_name (str):
        last_name (str):
        score (float): Final weighted score (0.0 - 1.0).
        score_breakdown (ScoreBreakdown): Per-factor contribution to the final recommendation score.
        headline (None | str | Unset):
        profile_image (None | str | Unset):
        role (None | str | Unset):
        experience_level (None | str | Unset):
        open_to_work (bool | Unset):  Default: True.
        location (None | str | Unset):
        matched_skills (list[str] | Unset): Normalized names of skills that matched the requirement.
        matched_technologies (list[str] | Unset): Project tech-stack items matched by the builder.
        contribution_count (int | Unset): Total prior contributions (accepted applications + projects). Default: 0.
    """

    user_id: UUID
    username: str
    first_name: str
    last_name: str
    score: float
    score_breakdown: ScoreBreakdown
    headline: None | str | Unset = UNSET
    profile_image: None | str | Unset = UNSET
    role: None | str | Unset = UNSET
    experience_level: None | str | Unset = UNSET
    open_to_work: bool | Unset = True
    location: None | str | Unset = UNSET
    matched_skills: list[str] | Unset = UNSET
    matched_technologies: list[str] | Unset = UNSET
    contribution_count: int | Unset = 0
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        user_id = str(self.user_id)

        username = self.username

        first_name = self.first_name

        last_name = self.last_name

        score = self.score

        score_breakdown = self.score_breakdown.to_dict()

        headline: None | str | Unset
        if isinstance(self.headline, Unset):
            headline = UNSET
        else:
            headline = self.headline

        profile_image: None | str | Unset
        if isinstance(self.profile_image, Unset):
            profile_image = UNSET
        else:
            profile_image = self.profile_image

        role: None | str | Unset
        if isinstance(self.role, Unset):
            role = UNSET
        else:
            role = self.role

        experience_level: None | str | Unset
        if isinstance(self.experience_level, Unset):
            experience_level = UNSET
        else:
            experience_level = self.experience_level

        open_to_work = self.open_to_work

        location: None | str | Unset
        if isinstance(self.location, Unset):
            location = UNSET
        else:
            location = self.location

        matched_skills: list[str] | Unset = UNSET
        if not isinstance(self.matched_skills, Unset):
            matched_skills = self.matched_skills

        matched_technologies: list[str] | Unset = UNSET
        if not isinstance(self.matched_technologies, Unset):
            matched_technologies = self.matched_technologies

        contribution_count = self.contribution_count

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "user_id": user_id,
                "username": username,
                "first_name": first_name,
                "last_name": last_name,
                "score": score,
                "score_breakdown": score_breakdown,
            }
        )
        if headline is not UNSET:
            field_dict["headline"] = headline
        if profile_image is not UNSET:
            field_dict["profile_image"] = profile_image
        if role is not UNSET:
            field_dict["role"] = role
        if experience_level is not UNSET:
            field_dict["experience_level"] = experience_level
        if open_to_work is not UNSET:
            field_dict["open_to_work"] = open_to_work
        if location is not UNSET:
            field_dict["location"] = location
        if matched_skills is not UNSET:
            field_dict["matched_skills"] = matched_skills
        if matched_technologies is not UNSET:
            field_dict["matched_technologies"] = matched_technologies
        if contribution_count is not UNSET:
            field_dict["contribution_count"] = contribution_count

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.score_breakdown import ScoreBreakdown

        d = dict(src_dict)
        user_id = UUID(d.pop("user_id"))

        username = d.pop("username")

        first_name = d.pop("first_name")

        last_name = d.pop("last_name")

        score = d.pop("score")

        score_breakdown = ScoreBreakdown.from_dict(d.pop("score_breakdown"))

        def _parse_headline(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        headline = _parse_headline(d.pop("headline", UNSET))

        def _parse_profile_image(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        profile_image = _parse_profile_image(d.pop("profile_image", UNSET))

        def _parse_role(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        role = _parse_role(d.pop("role", UNSET))

        def _parse_experience_level(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        experience_level = _parse_experience_level(d.pop("experience_level", UNSET))

        open_to_work = d.pop("open_to_work", UNSET)

        def _parse_location(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        location = _parse_location(d.pop("location", UNSET))

        matched_skills = cast(list[str], d.pop("matched_skills", UNSET))

        matched_technologies = cast(list[str], d.pop("matched_technologies", UNSET))

        contribution_count = d.pop("contribution_count", UNSET)

        recommended_builder = cls(
            user_id=user_id,
            username=username,
            first_name=first_name,
            last_name=last_name,
            score=score,
            score_breakdown=score_breakdown,
            headline=headline,
            profile_image=profile_image,
            role=role,
            experience_level=experience_level,
            open_to_work=open_to_work,
            location=location,
            matched_skills=matched_skills,
            matched_technologies=matched_technologies,
            contribution_count=contribution_count,
        )

        recommended_builder.additional_properties = d
        return recommended_builder

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
