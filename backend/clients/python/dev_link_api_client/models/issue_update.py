from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.issue_priority import IssuePriority
from ..models.issue_status import IssueStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="IssueUpdate")


@_attrs_define
class IssueUpdate:
    """
    Attributes:
        title (None | str | Unset):
        description (None | str | Unset):
        status (IssueStatus | None | Unset):
        priority (IssuePriority | None | Unset):
        labels (None | str | Unset):
    """

    title: None | str | Unset = UNSET
    description: None | str | Unset = UNSET
    status: IssueStatus | None | Unset = UNSET
    priority: IssuePriority | None | Unset = UNSET
    labels: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        title: None | str | Unset
        if isinstance(self.title, Unset):
            title = UNSET
        else:
            title = self.title

        description: None | str | Unset
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        status: None | str | Unset
        if isinstance(self.status, Unset):
            status = UNSET
        elif isinstance(self.status, IssueStatus):
            status = self.status.value
        else:
            status = self.status

        priority: None | str | Unset
        if isinstance(self.priority, Unset):
            priority = UNSET
        elif isinstance(self.priority, IssuePriority):
            priority = self.priority.value
        else:
            priority = self.priority

        labels: None | str | Unset
        if isinstance(self.labels, Unset):
            labels = UNSET
        else:
            labels = self.labels

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if title is not UNSET:
            field_dict["title"] = title
        if description is not UNSET:
            field_dict["description"] = description
        if status is not UNSET:
            field_dict["status"] = status
        if priority is not UNSET:
            field_dict["priority"] = priority
        if labels is not UNSET:
            field_dict["labels"] = labels

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_title(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        title = _parse_title(d.pop("title", UNSET))

        def _parse_description(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        description = _parse_description(d.pop("description", UNSET))

        def _parse_status(data: object) -> IssueStatus | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                status_type_0 = IssueStatus(data)

                return status_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(IssueStatus | None | Unset, data)

        status = _parse_status(d.pop("status", UNSET))

        def _parse_priority(data: object) -> IssuePriority | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                priority_type_0 = IssuePriority(data)

                return priority_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(IssuePriority | None | Unset, data)

        priority = _parse_priority(d.pop("priority", UNSET))

        def _parse_labels(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        labels = _parse_labels(d.pop("labels", UNSET))

        issue_update = cls(
            title=title,
            description=description,
            status=status,
            priority=priority,
            labels=labels,
        )

        issue_update.additional_properties = d
        return issue_update

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
