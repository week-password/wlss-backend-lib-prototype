from __future__ import annotations

import os
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Generic, TYPE_CHECKING, TypeVar

from typing_extensions import override

from wlss.exceptions import NO_TRACEBACK, ValidationError


if TYPE_CHECKING:
    import re
    from datetime import timezone
    from typing import Self


T = TypeVar("T")


class Type(ABC, Generic[T]):
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
    @abstractmethod
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


class PositiveInt(Int):
    VALUE_MIN = Int(0)


class Str(Type[str]):
    LENGTH_MAX: PositiveInt | None = None
    LENGTH_MIN: PositiveInt = PositiveInt(0)
    REGEXP: re.Pattern[str] | None = None

    @override
    def __init_subclass__(cls: type[Str]) -> None:
        super().__init_subclass__()
        if cls.LENGTH_MAX is not None and cls.LENGTH_MIN.value > cls.LENGTH_MAX.value:
            msg = "LENGTH_MAX should not be less than LENGTH_MIN."
            raise ValidationError(msg)

    @override
    @classmethod
    def validate(cls: type[Str], value: str) -> str:
        value = cls.validate_length_max(value)
        value = cls.validate_length_min(value)
        value = cls.validate_regexp(value)
        return value  # noqa: RET504

    @classmethod
    def validate_length_max(cls: type[Str], value: str) -> str:
        if cls.LENGTH_MAX is not None and len(value) > cls.LENGTH_MAX.value:
            msg = f"{cls.__name__} value length should not be greater than {cls.LENGTH_MAX.value}."
            raise ValidationError(msg)
        return value

    @classmethod
    def validate_length_min(cls: type[Str], value: str) -> str:
        if cls.LENGTH_MIN is not None and len(value) < cls.LENGTH_MIN.value:
            msg = f"{cls.__name__} value length should not be less than {cls.LENGTH_MIN.value}."
            raise ValidationError(msg)
        return value

    @classmethod
    def validate_regexp(cls: type[Str], value: str) -> str:
        if cls.REGEXP is not None and not cls.REGEXP.fullmatch(value):
            msg = rf"{cls.__name__} value should match regular expression: {cls.REGEXP.pattern}"
            raise ValidationError(msg)
        return value


class DatetimeType(Type[datetime], ABC):
    VALUE_MAX: DatetimeType | None = None
    VALUE_MIN: DatetimeType | None = None

    @override
    def __init_subclass__(cls: type[DatetimeType]) -> None:
        super().__init_subclass__()
        if cls.VALUE_MAX is not None and cls.VALUE_MIN is not None and cls.VALUE_MAX.value < cls.VALUE_MIN.value:
            msg = "VALUE_MAX should not be less than VALUE_MIN."
            raise ValidationError(msg)

    @override
    @classmethod
    def validate(cls: type[DatetimeType], value: datetime) -> datetime:
        value = cls.validate_timezone(value)
        value = cls.validate_value_max(value)
        value = cls.validate_value_min(value)
        return value  # noqa: RET504

    @classmethod
    @abstractmethod
    def validate_timezone(cls: type[DatetimeType], value: datetime) -> datetime:
        raise NotImplementedError  # pragma: no cover

    @classmethod
    def validate_value_max(cls: type[DatetimeType], value: datetime) -> datetime:
        if cls.VALUE_MAX is not None and value > cls.VALUE_MAX.value:
            msg = f"{cls.__name__} value should not be greater than {cls.VALUE_MAX.value}."
            raise ValidationError(msg)
        return value

    @classmethod
    def validate_value_min(cls: type[DatetimeType], value: datetime) -> datetime:
        if cls.VALUE_MIN is not None and value < cls.VALUE_MIN.value:
            msg = f"{cls.__name__} value should not be less than {cls.VALUE_MIN.value}."
            raise ValidationError(msg)
        return value


class NaiveDatetime(DatetimeType):
    VALUE_MAX: NaiveDatetime | None = None
    VALUE_MIN: NaiveDatetime | None = None

    @override
    @classmethod
    def validate_timezone(cls: type[NaiveDatetime], value: datetime) -> datetime:
        if value.tzinfo is not None:
            msg = f"{cls.__name__} value should be timezone-naive."
            raise ValidationError(msg)
        return value


class AwareDatetime(DatetimeType):
    VALUE_MAX: AwareDatetime | None = None
    VALUE_MIN: AwareDatetime | None = None
    TIMEZONE: timezone | None = None

    @override
    @classmethod
    def validate_timezone(cls: type[AwareDatetime], value: datetime) -> datetime:
        if value.tzinfo is None:
            msg = f"{cls.__name__} value should be timezone-aware datetime."
            raise ValidationError(msg)
        if cls.TIMEZONE is not None and value.tzinfo != cls.TIMEZONE:
            msg = f"{cls.__name__} value should be timezone-aware datetime in {cls.TIMEZONE} timezone."
            raise ValidationError(msg)
        return value
