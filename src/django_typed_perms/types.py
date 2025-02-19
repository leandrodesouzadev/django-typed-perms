from typing import Any, Protocol, Sequence
from typing import Literal
from typing_extensions import TypeVar


_DjangoDefaultModelPerms = Literal["add", "change", "delete", "view"]

CustomPermsT = TypeVar("CustomPermsT", default=_DjangoDefaultModelPerms)
DjangoModelPermsT = TypeVar("ModelPermsT", default=_DjangoDefaultModelPerms)


class UserProtocol(Protocol):
    is_active: bool
    is_staff: bool
    is_superuser: bool

    def has_perm(self, perm: str, obj: Any | None = None) -> bool: ...
    def has_perms(self, perm_list: Sequence[str], obj: Any | None = None) -> bool: ...
