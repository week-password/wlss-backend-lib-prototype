from __future__ import annotations

from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from typing import Self


# special constant which is used to detect place where traceback should be cut off (see wlss_excepthook for usage)
NO_TRACEBACK = None


class ValidationError(ValueError):
    def __init__(self: Self, msg: str) -> None:
        self.msg = msg
