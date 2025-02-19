from collections.abc import Sequence
from typing import Any, Generic, get_args

from . import types


class TypedPermsModelMixin(Generic[types.CustomPermsT, types.DjangoModelPermsT]):
    @classmethod
    def get_action_permission_name(
        cls, action: types.CustomPermsT | types.DjangoModelPermsT
    ) -> str:
        is_default_model_perm = action in get_args(types._DjangoDefaultModelPerms)

        if is_default_model_perm:
            codename = f"{action}_{cls._meta.model_name}"
        else:
            codename = action
        return f"{cls._meta.app_label}.{codename}"

    @classmethod
    def user_has_permission(
        cls,
        user: types.UserProtocol | None,
        action: types.CustomPermsT | types.DjangoModelPermsT,
        obj: Any | None = None,
    ) -> bool:
        perm = cls.get_action_permission_name(action)
        return user is not None and user.has_perm(perm, obj=obj)

    @classmethod
    def user_has_permissions(
        cls,
        user: types.UserProtocol | None,
        actions: Sequence[types.CustomPermsT | types.DjangoModelPermsT],
        obj: Any | None = None,
    ) -> bool:
        perms = [cls.get_action_permission_name(a) for a in actions]
        return user is not None and user.has_perms(perms, obj=obj)
