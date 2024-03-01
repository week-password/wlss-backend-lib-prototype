from __future__ import annotations

from wlss.core.types import Int, PositiveInt
from wlss.file.constants import BYTE, MEGABYTE


class FileSize(PositiveInt):
    VALUE_MAX = Int(10 * MEGABYTE)
    VALUE_MIN = Int(1 * BYTE)
