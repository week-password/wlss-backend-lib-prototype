# mypy: disable-error-code="no-untyped-def"
from __future__ import annotations

import re
import subprocess
import sys
import textwrap
from datetime import datetime, timedelta, timezone

import pytest

from wlss.core.exceptions import ValidationError
from wlss.core.types import AwareDatetime, Int, NaiveDatetime, PositiveInt, Str


class Test_Int:  # noqa: N801

    @staticmethod
    def test_when_initialized_by_object_of_type_Type():
        result = Int(Int(42))

        assert result.value == 42

    @staticmethod
    def test_when_value_less_than_VALUE_MIN():
        class MyInt(Int):
            VALUE_MIN = Int(0)

        with pytest.raises(ValidationError) as exc_info:
            MyInt(-42)

        assert exc_info.type is ValidationError
        assert exc_info.value.args == ("MyInt value should not be less than 0.", )


    @staticmethod
    def test_when_value_greater_than_VALUE_MAX():
        class MyInt(Int):
            VALUE_MAX = Int(0)

        with pytest.raises(ValidationError) as exc_info:
            MyInt(42)

        assert exc_info.type is ValidationError
        assert exc_info.value.args == ("MyInt value should not be greater than 0.", )


    @staticmethod
    def test_when_subclass_has_VALUE_MIN_greater_than_VALUE_MAX():
        with pytest.raises(ValidationError) as exc_info:
            class MyInt(Int):
                VALUE_MIN = Int(42)
                VALUE_MAX = Int(0)

        assert exc_info.type is ValidationError
        assert exc_info.value.args == ("VALUE_MAX should not be less than VALUE_MIN.", )

    @staticmethod
    def test_when_object_compared_to_another_object():
        assert Int(42) == Int(42)

    @staticmethod
    def test_when_object_compared_to_another_object_of_different_class():
        class FooInt(Int):
            ...
        class BarInt(Int):
            ...

        assert FooInt(42) != BarInt(42)

    @staticmethod
    def test_when_object_is_hashed():
        assert hash(Int(42)) == hash(42)


    @staticmethod
    def test_when_WLSS_LIB_TRACEBACK_is_not_set(tmp_path):
        """Test that traceback is fully printed to the console if WLSS_LIB_TRACEBACK is not set.

        This test runs script in standalone process because we cannot raise exceptions
        within the same process where this test runs.

        Also we check only last several lines of traceback because other lines before are strongly dependant of
        file structures. For example "File /foo/bar/wlss/types.py at line 24" can be different depending on
        our wlss codebase, that's why we cannot assert full traceback and have to check only last lines.
        """
        py_file = tmp_path / "script.py"
        py_file.write_text(textwrap.dedent("""
            from wlss.core.types import Int
            class MyInt(Int):
                VALUE_MIN = Int(0)

            foo = MyInt(-10)
        """))

        result = subprocess.run(
            [sys.executable, str(py_file)],  # noqa: S603
            capture_output=True,
            check=False,
        )

        assert result.returncode == 1
        assert result.stderr.decode("utf-8").split("\n")[-3:] == [
            "    raise ValidationError(msg)",
            "wlss.core.exceptions.ValidationError: MyInt value should not be less than 0.",
            "",
        ]


    @staticmethod
    def test_when_WLSS_LIB_TRACEBACK_is_set_to_disabled(tmp_path):
        """Test that 'wlss' lib related traceback is cut off if WLSS_LIB_TRACEBACK="disable".

        This test runs script in standalone process because we cannot raise exceptions
        within the same process where this test runs.

        Also we check only last several lines of traceback because other lines before are strongly dependant of
        file structures. For example "File /foo/bar/wlss/types.py at line 24" can be different depending on
        our wlss codebase, that's why we cannot assert full traceback and have to check only last lines.
        """
        py_file = tmp_path / "script.py"
        py_file.write_text(textwrap.dedent("""
            from wlss.core.types import Int
            class MyInt(Int):
                VALUE_MIN = Int(0)

            foo = MyInt(-10)
        """))

        result = subprocess.run(
            [sys.executable, str(py_file)],  # noqa: S603
            capture_output=True,
            check=False,
            env={"WLSS_LIB_TRACEBACK": "disable"},
        )

        assert result.returncode == 1
        assert result.stderr.decode("utf-8").split("\n")[-10:] == [
            "    foo = MyInt(-10)",
            "          ^^^^^^^^^^",
            "wlss.core.exceptions.ValidationError: MyInt value should not be less than 0.",
            "",
            "<...>",
            "",
            "Rest of the traceback related to 'wlss' lib was cut off for the sake of readibility.",
            'If you need to have full traceback set WLSS_LIB_TB="true" environment variable.',
            "",
            "",
        ]


class Test_Str:  # noqa: N801
    @staticmethod
    def test_when_value_is_correct():
        class MyStr(Str):
            LENGTH_MIN = PositiveInt(1)
            LENGTH_MAX = PositiveInt(5)

        result = MyStr("foo")

        assert result.value == "foo"

    @staticmethod
    def test_when_value_length_less_than_LENGTH_MIN():
        class MyStr(Str):
            LENGTH_MIN = PositiveInt(10)

        with pytest.raises(ValidationError) as exc_info:
            MyStr("foo")

        assert exc_info.type is ValidationError
        assert exc_info.value.args == ("MyStr value length should not be less than 10.", )


    @staticmethod
    def test_when_value_length_greater_than_LENGTH_MAX():
        class MyStr(Str):
            LENGTH_MAX = PositiveInt(2)

        with pytest.raises(ValidationError) as exc_info:
            MyStr("foo")

        assert exc_info.type is ValidationError
        assert exc_info.value.args == ("MyStr value length should not be greater than 2.", )

    @staticmethod
    def test_when_subclass_has_LENGTH_MIN_greater_than_LENGTH_MAX():
        with pytest.raises(ValidationError) as exc_info:
            class MyStr(Str):
                LENGTH_MAX = PositiveInt(0)
                LENGTH_MIN = PositiveInt(42)

        assert exc_info.type is ValidationError
        assert exc_info.value.args == ("LENGTH_MAX should not be less than LENGTH_MIN.", )

    @staticmethod
    def test_when_value_does_not_match_REGEXP():
        class MyStr(Str):
            REGEXP = re.compile(r"bar")

        with pytest.raises(ValidationError) as exc_info:
            MyStr("foo")

        assert exc_info.type is ValidationError
        assert exc_info.value.args == ("MyStr value should match regular expression: bar", )


class Test_NaiveDatetime:  # noqa: N801

    @staticmethod
    def test_when_subclass_has_VALUE_MIN_greater_than_VALUE_MAX():
        with pytest.raises(ValidationError) as exc_info:
            class MyDatetime(NaiveDatetime):
                VALUE_MAX = NaiveDatetime(datetime.now())  # noqa: DTZ005
                VALUE_MIN = NaiveDatetime(datetime.now() + timedelta(days=1))  # noqa: DTZ005

        assert exc_info.type is ValidationError
        assert exc_info.value.args == ("VALUE_MAX should not be less than VALUE_MIN.", )

    @staticmethod
    def test_when_value_is_correct():
        current_datetime = datetime.now()  # noqa: DTZ005
        result = NaiveDatetime(current_datetime)

        assert result.value == current_datetime
        assert result.value.tzinfo is None

    @staticmethod
    def test_when_initialized_with_not_naive_datetime():
        with pytest.raises(ValidationError) as exc_info:
            NaiveDatetime(datetime.now(tz=timezone.utc))

        assert exc_info.type is ValidationError
        assert exc_info.value.args == ("NaiveDatetime value should be timezone-naive.", )

    @staticmethod
    def test_when_value_greater_than_VALUE_MAX():
        value_max = datetime.now()  # noqa: DTZ005
        greater_than_max = value_max + timedelta(days=1)
        class MyNaiveDatetime(NaiveDatetime):
            VALUE_MAX = NaiveDatetime(value_max)

        with pytest.raises(ValidationError) as exc_info:
            MyNaiveDatetime(greater_than_max)

        assert exc_info.type is ValidationError
        assert exc_info.value.args == (f"MyNaiveDatetime value should not be greater than {value_max}.", )

    @staticmethod
    def test_when_value_less_than_VALUE_MIN():
        value_min = datetime.now()  # noqa: DTZ005
        less_than_max = value_min - timedelta(days=1)
        class MyNaiveDatetime(NaiveDatetime):
            VALUE_MIN = NaiveDatetime(value_min)

        with pytest.raises(ValidationError) as exc_info:
            MyNaiveDatetime(less_than_max)

        assert exc_info.type is ValidationError
        assert exc_info.value.args == (f"MyNaiveDatetime value should not be less than {value_min}.", )


class Test_AwareDatetime:  # noqa: N801
    @staticmethod
    def test_when_value_is_correct():
        current_datetime = datetime.now(tz=timezone.utc)
        class MyAwareDatetime(AwareDatetime):
            TIMEZONE = timezone.utc

        result = MyAwareDatetime(current_datetime)

        assert result.value == current_datetime

    @staticmethod
    def test_initialized_by_naive_datetime():
        with pytest.raises(ValidationError) as exc_info:
            AwareDatetime(datetime.now())  # noqa: DTZ005

        assert exc_info.type is ValidationError
        assert exc_info.value.args == ("AwareDatetime value should be timezone-aware datetime.", )

    @staticmethod
    def test_initialized_by_datetime_with_wrong_timezone():
        class MyAwareDatetime(AwareDatetime):
            TIMEZONE = timezone(offset=timedelta(hours=3))

        with pytest.raises(ValidationError) as exc_info:
            MyAwareDatetime(datetime.now(tz=timezone.utc))

        assert exc_info.type is ValidationError
        assert exc_info.value.args == (
            "MyAwareDatetime value should be timezone-aware datetime in UTC+03:00 timezone.",
        )
