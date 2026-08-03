from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.current_user import CurrentUser


T = TypeVar("T", bound="AuthResponse")


@_attrs_define
class AuthResponse:
    """
    Attributes:
        message (str):
        success (bool | Unset):  Default: True.
        access_token (None | str | Unset):
        refresh_token (None | str | Unset):
        token_type (None | str | Unset):  Default: 'bearer'.
        mfa_required (bool | Unset):  Default: False.
        mfa_token (None | str | Unset):
        user (CurrentUser | None | Unset):
    """

    message: str
    success: bool | Unset = True
    access_token: None | str | Unset = UNSET
    refresh_token: None | str | Unset = UNSET
    token_type: None | str | Unset = "bearer"
    mfa_required: bool | Unset = False
    mfa_token: None | str | Unset = UNSET
    user: CurrentUser | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.current_user import CurrentUser

        message = self.message

        success = self.success

        access_token: None | str | Unset
        if isinstance(self.access_token, Unset):
            access_token = UNSET
        else:
            access_token = self.access_token

        refresh_token: None | str | Unset
        if isinstance(self.refresh_token, Unset):
            refresh_token = UNSET
        else:
            refresh_token = self.refresh_token

        token_type: None | str | Unset
        if isinstance(self.token_type, Unset):
            token_type = UNSET
        else:
            token_type = self.token_type

        mfa_required = self.mfa_required

        mfa_token: None | str | Unset
        if isinstance(self.mfa_token, Unset):
            mfa_token = UNSET
        else:
            mfa_token = self.mfa_token

        user: dict[str, Any] | None | Unset
        if isinstance(self.user, Unset):
            user = UNSET
        elif isinstance(self.user, CurrentUser):
            user = self.user.to_dict()
        else:
            user = self.user

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "message": message,
            }
        )
        if success is not UNSET:
            field_dict["success"] = success
        if access_token is not UNSET:
            field_dict["access_token"] = access_token
        if refresh_token is not UNSET:
            field_dict["refresh_token"] = refresh_token
        if token_type is not UNSET:
            field_dict["token_type"] = token_type
        if mfa_required is not UNSET:
            field_dict["mfa_required"] = mfa_required
        if mfa_token is not UNSET:
            field_dict["mfa_token"] = mfa_token
        if user is not UNSET:
            field_dict["user"] = user

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.current_user import CurrentUser

        d = dict(src_dict)
        message = d.pop("message")

        success = d.pop("success", UNSET)

        def _parse_access_token(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        access_token = _parse_access_token(d.pop("access_token", UNSET))

        def _parse_refresh_token(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        refresh_token = _parse_refresh_token(d.pop("refresh_token", UNSET))

        def _parse_token_type(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        token_type = _parse_token_type(d.pop("token_type", UNSET))

        mfa_required = d.pop("mfa_required", UNSET)

        def _parse_mfa_token(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        mfa_token = _parse_mfa_token(d.pop("mfa_token", UNSET))

        def _parse_user(data: object) -> CurrentUser | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                user_type_0 = CurrentUser.from_dict(data)

                return user_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(CurrentUser | None | Unset, data)

        user = _parse_user(d.pop("user", UNSET))

        auth_response = cls(
            message=message,
            success=success,
            access_token=access_token,
            refresh_token=refresh_token,
            token_type=token_type,
            mfa_required=mfa_required,
            mfa_token=mfa_token,
            user=user,
        )

        auth_response.additional_properties = d
        return auth_response

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
