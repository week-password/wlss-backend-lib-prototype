# mypy: disable-error-code="no-untyped-def"
from __future__ import annotations

import subprocess
import sys
import textwrap

import pytest

from wlss.exceptions import ValidationError
from wlss.types import Int


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
            from wlss.types import Int
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
            "wlss.exceptions.ValidationError: MyInt value should not be less than 0.",
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
            import sys
            print(sys.version)
            from wlss.types import Int
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
            "wlss.exceptions.ValidationError: MyInt value should not be less than 0.",
            "",
            "<...>",
            "",
            "Rest of the traceback related to 'wlss' lib was cut off for the sake of readibility.",
            'If you need to have full traceback set WLSS_LIB_TB="true" environment variable.',
            "",
            "",
        ]
