from __future__ import annotations

import os
from typing import Generic, TYPE_CHECKING, TypeVar

from typing_extensions import override

from wlss.exceptions import NO_TRACEBACK, ValidationError


if TYPE_CHECKING:
    from typing import Self


T = TypeVar("T")


class Type(Generic[T]):
    def __init__(self: Self, value: T | Type[T]) -> None:
        if isinstance(value, Type):
            value = value.value
        try:
            self._value = self.validate(value)
        except ValidationError as e:
            if os.environ.get("WLSS_LIB_TRACEBACK") == "disable":
                # the line below is actually covered but coverage isn't recorded
                # because test for this functionality has to run script in a standalone process
                raise e.with_traceback(NO_TRACEBACK) from None  # pragma: no cover
            raise e

    @classmethod
    def validate(cls: type[Type[T]], value: T) -> T:
        raise NotImplementedError  # pragma: no cover

    @property
    def value(self: Self) -> T:
        return self._value



class Int(Type[int]):
    VALUE_MAX: Int | None = None
    VALUE_MIN: Int | None = None

    @override
    def __init_subclass__(cls: type[Int]) -> None:
        super().__init_subclass__()
        if cls.VALUE_MAX is not None and cls.VALUE_MIN is not None and cls.VALUE_MIN.value > cls.VALUE_MAX.value:
            msg = "VALUE_MAX should not be less than VALUE_MIN."
            raise ValidationError(msg)

    @override
    @classmethod
    def validate(cls: type[Int], value: int) -> int:
        value = cls.validate_value_max(value)
        value = cls.validate_value_min(value)
        return value  # noqa: RET504

    @classmethod
    def validate_value_max(cls: type[Int], value: int) -> int:
        if cls.VALUE_MAX is not None and value > cls.VALUE_MAX.value:
            msg = f"{cls.__name__} value should not be greater than {cls.VALUE_MAX.value}."
            raise ValidationError(msg)
        return value

    @classmethod
    def validate_value_min(cls: type[Int], value: int) -> int:
        if cls.VALUE_MIN is not None and value < cls.VALUE_MIN.value:
            msg = f"{cls.__name__} value should not be less than {cls.VALUE_MIN.value}."
            raise ValidationError(msg)
        return value
