from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.score_breakdown import ScoreBreakdown


T = TypeVar("T", bound="RecommendedProject")


@_attrs_define
class RecommendedProject:
    """A single project recommendation entry.

    Attributes:
        project_id (UUID):
        title (str):
        owner_username (str):
        status (str):
        score (float): Final weighted score (0.0 - 1.0).
        score_breakdown (ScoreBreakdown): Per-factor contribution to the final recommendation score.
        description (None | str | Unset):
        tech_stack (None | str | Unset):
        minimum_experience (int | Unset):  Default: 0.
        matched_skills (list[str] | Unset): Normalized names of required skills that matched the builder.
        matched_technologies (list[str] | Unset): Project tech-stack items matched by the builder.
    """

    project_id: UUID
    title: str
    owner_username: str
    status: str
    score: float
    score_breakdown: ScoreBreakdown
    description: None | str | Unset = UNSET
    tech_stack: None | str | Unset = UNSET
    minimum_experience: int | Unset = 0
    matched_skills: list[str] | Unset = UNSET
    matched_technologies: list[str] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        project_id = str(self.project_id)

        title = self.title

        owner_username = self.owner_username

        status = self.status

        score = self.score

        score_breakdown = self.score_breakdown.to_dict()

        description: None | str | Unset
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        tech_stack: None | str | Unset
        if isinstance(self.tech_stack, Unset):
            tech_stack = UNSET
        else:
            tech_stack = self.tech_stack

        minimum_experience = self.minimum_experience

        matched_skills: list[str] | Unset = UNSET
        if not isinstance(self.matched_skills, Unset):
            matched_skills = self.matched_skills

        matched_technologies: list[str] | Unset = UNSET
        if not isinstance(self.matched_technologies, Unset):
            matched_technologies = self.matched_technologies

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "project_id": project_id,
                "title": title,
                "owner_username": owner_username,
                "status": status,
                "score": score,
                "score_breakdown": score_breakdown,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if tech_stack is not UNSET:
            field_dict["tech_stack"] = tech_stack
        if minimum_experience is not UNSET:
            field_dict["minimum_experience"] = minimum_experience
        if matched_skills is not UNSET:
            field_dict["matched_skills"] = matched_skills
        if matched_technologies is not UNSET:
            field_dict["matched_technologies"] = matched_technologies

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.score_breakdown import ScoreBreakdown

        d = dict(src_dict)
        project_id = UUID(d.pop("project_id"))

        title = d.pop("title")

        owner_username = d.pop("owner_username")

        status = d.pop("status")

        score = d.pop("score")

        score_breakdown = ScoreBreakdown.from_dict(d.pop("score_breakdown"))

        def _parse_description(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        description = _parse_description(d.pop("description", UNSET))

        def _parse_tech_stack(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        tech_stack = _parse_tech_stack(d.pop("tech_stack", UNSET))

        minimum_experience = d.pop("minimum_experience", UNSET)

        matched_skills = cast(list[str], d.pop("matched_skills", UNSET))

        matched_technologies = cast(list[str], d.pop("matched_technologies", UNSET))

        recommended_project = cls(
            project_id=project_id,
            title=title,
            owner_username=owner_username,
            status=status,
            score=score,
            score_breakdown=score_breakdown,
            description=description,
            tech_stack=tech_stack,
            minimum_experience=minimum_experience,
            matched_skills=matched_skills,
            matched_technologies=matched_technologies,
        )

        recommended_project.additional_properties = d
        return recommended_project

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
