from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.notification_type import NotificationType
from ..types import UNSET, Unset

T = TypeVar("T", bound="NotificationCreate")


@_attrs_define
class NotificationCreate:
    """
    Attributes:
        recipient_id (UUID):
        type_ (NotificationType):
        title (str):
        message (str):
        action_url (None | str | Unset):
        image_url (None | str | Unset):
        project_id (None | Unset | UUID):
        conversation_id (None | Unset | UUID):
        message_id (None | Unset | UUID):
        application_id (None | Unset | UUID):
    """

    recipient_id: UUID
    type_: NotificationType
    title: str
    message: str
    action_url: None | str | Unset = UNSET
    image_url: None | str | Unset = UNSET
    project_id: None | Unset | UUID = UNSET
    conversation_id: None | Unset | UUID = UNSET
    message_id: None | Unset | UUID = UNSET
    application_id: None | Unset | UUID = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        recipient_id = str(self.recipient_id)

        type_ = self.type_.value

        title = self.title

        message = self.message

        action_url: None | str | Unset
        if isinstance(self.action_url, Unset):
            action_url = UNSET
        else:
            action_url = self.action_url

        image_url: None | str | Unset
        if isinstance(self.image_url, Unset):
            image_url = UNSET
        else:
            image_url = self.image_url

        project_id: None | str | Unset
        if isinstance(self.project_id, Unset):
            project_id = UNSET
        elif isinstance(self.project_id, UUID):
            project_id = str(self.project_id)
        else:
            project_id = self.project_id

        conversation_id: None | str | Unset
        if isinstance(self.conversation_id, Unset):
            conversation_id = UNSET
        elif isinstance(self.conversation_id, UUID):
            conversation_id = str(self.conversation_id)
        else:
            conversation_id = self.conversation_id

        message_id: None | str | Unset
        if isinstance(self.message_id, Unset):
            message_id = UNSET
        elif isinstance(self.message_id, UUID):
            message_id = str(self.message_id)
        else:
            message_id = self.message_id

        application_id: None | str | Unset
        if isinstance(self.application_id, Unset):
            application_id = UNSET
        elif isinstance(self.application_id, UUID):
            application_id = str(self.application_id)
        else:
            application_id = self.application_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "recipient_id": recipient_id,
                "type": type_,
                "title": title,
                "message": message,
            }
        )
        if action_url is not UNSET:
            field_dict["action_url"] = action_url
        if image_url is not UNSET:
            field_dict["image_url"] = image_url
        if project_id is not UNSET:
            field_dict["project_id"] = project_id
        if conversation_id is not UNSET:
            field_dict["conversation_id"] = conversation_id
        if message_id is not UNSET:
            field_dict["message_id"] = message_id
        if application_id is not UNSET:
            field_dict["application_id"] = application_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        recipient_id = UUID(d.pop("recipient_id"))

        type_ = NotificationType(d.pop("type"))

        title = d.pop("title")

        message = d.pop("message")

        def _parse_action_url(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        action_url = _parse_action_url(d.pop("action_url", UNSET))

        def _parse_image_url(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        image_url = _parse_image_url(d.pop("image_url", UNSET))

        def _parse_project_id(data: object) -> None | Unset | UUID:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                project_id_type_0 = UUID(data)

                return project_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | Unset | UUID, data)

        project_id = _parse_project_id(d.pop("project_id", UNSET))

        def _parse_conversation_id(data: object) -> None | Unset | UUID:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                conversation_id_type_0 = UUID(data)

                return conversation_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | Unset | UUID, data)

        conversation_id = _parse_conversation_id(d.pop("conversation_id", UNSET))

        def _parse_message_id(data: object) -> None | Unset | UUID:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                message_id_type_0 = UUID(data)

                return message_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | Unset | UUID, data)

        message_id = _parse_message_id(d.pop("message_id", UNSET))

        def _parse_application_id(data: object) -> None | Unset | UUID:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                application_id_type_0 = UUID(data)

                return application_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | Unset | UUID, data)

        application_id = _parse_application_id(d.pop("application_id", UNSET))

        notification_create = cls(
            recipient_id=recipient_id,
            type_=type_,
            title=title,
            message=message,
            action_url=action_url,
            image_url=image_url,
            project_id=project_id,
            conversation_id=conversation_id,
            message_id=message_id,
            application_id=application_id,
        )

        notification_create.additional_properties = d
        return notification_create

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
