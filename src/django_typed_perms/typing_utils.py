from collections.abc import Generator
from typing import Sequence, TypeVar, get_args, Literal


AT = TypeVar("AT")  # AnnotatedType


def is_typing_type(t, expected_type: Literal["Literal", "Union", "Annotated"]) -> bool:
    return getattr(t, "__name__", "") == expected_type


def get_choices_from_type_hint(t: AT) -> Sequence[tuple[AT, str]]:
    if is_typing_type(t, "Annotated"):
        return (single_choice_from_annotated_type(t),)
    if is_typing_type(t, "Union"):
        return tuple(choices_from_union_type(t))
    raise ValueError("Value is neither Annotated/Union[Annotated]", t.__class__)


def single_choice_from_annotated_type(at: AT) -> tuple[AT, str]:
    annotation = get_args(at)
    if len(annotation) != 2:
        raise ValueError("Annotated type must have at least one metadata associated")
    lit, label = annotation
    if not is_typing_type(lit, "Literal"):
        raise ValueError("Annotated type must be a Literal type")

    # support for gettext_lazy
    lazy_label_args = getattr(label, "_args", [])
    if len(lazy_label_args) == 1 and isinstance(lazy_label_args[0], str):
        label = lazy_label_args[0]

    if label is not None and not isinstance(label, str):
        raise ValueError(
            "Annotated first metadata must be a `str` | `None`, got:",
            repr(label.__class__.__name__),
            f"Object repr: {label!r}",
        )

    db_values = get_args(lit)
    if len(db_values) > 1:
        raise ValueError(
            "Literal type must have only one value associated with it", db_values
        )

    return db_values[0], label


def choices_from_union_type(at: AT) -> Generator[tuple[AT, str]]:
    types = get_args(at)
    for t in types:
        if not is_typing_type(t, "Annotated"):
            raise ValueError("Union type must have only Annotated types, got:", repr(t))
        yield single_choice_from_annotated_type(t)
