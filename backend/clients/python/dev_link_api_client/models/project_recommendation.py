from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.recommendation_project import RecommendationProject


T = TypeVar("T", bound="ProjectRecommendation")


@_attrs_define
class ProjectRecommendation:
    """A single project recommendation with score and breakdown.

    Attributes:
        project (RecommendationProject): Simplified project representation for recommendation results.
            Includes key fields for display without heavy nesting.
        score (float):
        skill_match_count (int):
        total_skills (int):
        is_previous_contribution (bool):
        is_bookmarked (bool):
        is_org_related (bool):
    """

    project: RecommendationProject
    score: float
    skill_match_count: int
    total_skills: int
    is_previous_contribution: bool
    is_bookmarked: bool
    is_org_related: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        project = self.project.to_dict()

        score = self.score

        skill_match_count = self.skill_match_count

        total_skills = self.total_skills

        is_previous_contribution = self.is_previous_contribution

        is_bookmarked = self.is_bookmarked

        is_org_related = self.is_org_related

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "project": project,
                "score": score,
                "skill_match_count": skill_match_count,
                "total_skills": total_skills,
                "is_previous_contribution": is_previous_contribution,
                "is_bookmarked": is_bookmarked,
                "is_org_related": is_org_related,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.recommendation_project import RecommendationProject

        d = dict(src_dict)
        project = RecommendationProject.from_dict(d.pop("project"))

        score = d.pop("score")

        skill_match_count = d.pop("skill_match_count")

        total_skills = d.pop("total_skills")

        is_previous_contribution = d.pop("is_previous_contribution")

        is_bookmarked = d.pop("is_bookmarked")

        is_org_related = d.pop("is_org_related")

        project_recommendation = cls(
            project=project,
            score=score,
            skill_match_count=skill_match_count,
            total_skills=total_skills,
            is_previous_contribution=is_previous_contribution,
            is_bookmarked=is_bookmarked,
            is_org_related=is_org_related,
        )

        project_recommendation.additional_properties = d
        return project_recommendation

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
