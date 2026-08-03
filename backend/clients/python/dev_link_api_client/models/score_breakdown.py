from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ScoreBreakdown")


@_attrs_define
class ScoreBreakdown:
    """Per-factor contribution to the final recommendation score.

    Attributes:
        skills (float): Skill overlap between builder and project/seed profile.
        interests (float): Interest overlap (bio/headline keywords).
        experience (float): Experience level match vs. project requirement.
        technologies (float): Preferred-technology overlap with project tech stack.
        availability (float): Builder availability (open_to_work) signal.
        contributions (float): Previous-contribution track-record signal.
        network (float): Social-graph boost (mutual followers).
    """

    skills: float
    interests: float
    experience: float
    technologies: float
    availability: float
    contributions: float
    network: float
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        skills = self.skills

        interests = self.interests

        experience = self.experience

        technologies = self.technologies

        availability = self.availability

        contributions = self.contributions

        network = self.network

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "skills": skills,
                "interests": interests,
                "experience": experience,
                "technologies": technologies,
                "availability": availability,
                "contributions": contributions,
                "network": network,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        skills = d.pop("skills")

        interests = d.pop("interests")

        experience = d.pop("experience")

        technologies = d.pop("technologies")

        availability = d.pop("availability")

        contributions = d.pop("contributions")

        network = d.pop("network")

        score_breakdown = cls(
            skills=skills,
            interests=interests,
            experience=experience,
            technologies=technologies,
            availability=availability,
            contributions=contributions,
            network=network,
        )

        score_breakdown.additional_properties = d
        return score_breakdown

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
