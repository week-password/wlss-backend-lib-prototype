from __future__ import annotations

from wlss.core.types import Int, PositiveInt
from wlss.file.constants import BYTE, MEGABYTE


class FileSize(Int):
    VALUE_MAX = PositiveInt(10 * MEGABYTE)
    VALUE_MIN = PositiveInt(1 * BYTE)
