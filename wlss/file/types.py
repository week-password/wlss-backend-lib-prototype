from __future__ import annotations

from wlss.core.types import Int, PositiveInt, Str
from wlss.file.constants import BYTE, MEGABYTE


class FileName(Str):
    LENGTH_MIN = PositiveInt(1)
    LENGTH_MAX = PositiveInt(256)


class FileSize(PositiveInt):
    VALUE_MAX = Int(10 * MEGABYTE)
    VALUE_MIN = Int(1 * BYTE)
