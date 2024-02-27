from __future__ import annotations

import os
import sys
import textwrap
from pathlib import Path
from traceback import extract_tb, print_exception
from typing import TYPE_CHECKING

import wlss
from wlss.core.exceptions import ValidationError


if TYPE_CHECKING:
    from types import TracebackType


def wlss_excepthook(
    exception_type: type[BaseException],
    exception: BaseException,
    traceback: TracebackType | None,

    # the function below is actually covered but coverage isn't recorded
    # because test for this functionality has to run script in a standalone process
) -> None:  # pragma: no cover
    """Custom excepthook which cuts off traceback from 'wlss' lib."""

    """
    ==================================
    Programmer! Here is a DANGER zone!
    ==================================

    You have to be careful when editing code of this hook because if this function
    will have unhandled exception, then you will not see any output at all.
    Python doesn't have any other place to handle your error raised in this hook.
    Hence your script will just abort silently.
    """

    if exception_type is not ValidationError:
        # we want to cut only traceback from validation exception
        # which has been raised during user's input validation
        # any other unexpected error traceback shouldn't be cut off
        return sys.__excepthook__(exception_type, exception, traceback)

    wlss_lib_path = str(Path(wlss.__file__).parent.absolute())

    limit = 0
    for frame in extract_tb(traceback):
        if (
            frame.filename.startswith(wlss_lib_path)
            and frame.line is not None
            # if execution gets the line ended by the string below, then regular ValidationError happened
            # and wlss lib tracebacks are disabled, therefor in that case and we want to cut traceback off
            and frame.line.endswith(".with_traceback(NO_TRACEBACK) from None  # pragma: no cover")
        ):
            break
        limit += 1

    print_exception(exception, limit=limit)
    print(textwrap.dedent(f"""
        <...>

        Rest of the traceback related to '{wlss.__name__}' lib was cut off for the sake of readibility.
        If you need to have full traceback set WLSS_LIB_TB="true" environment variable.
    """), file=sys.stderr)  # noqa: T201

    return None


if os.environ.get("WLSS_LIB_TRACEBACK") == "disable":
    sys.excepthook = wlss_excepthook  # pragma: no cover
