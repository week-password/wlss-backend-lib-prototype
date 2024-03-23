from __future__ import annotations

import re

from wlss.core.types import PositiveInt, Str


class WishDescription(Str):
    LENGTH_MAX = PositiveInt(10_000)
    LENGTH_MIN = PositiveInt(1)
    REGEXP = re.compile(r".*", flags=re.DOTALL)


class WishTitle(Str):
    LENGTH_MAX = PositiveInt(100)
    LENGTH_MIN = PositiveInt(1)
    REGEXP = re.compile(r"[A-Za-zА-яЁё'-.() ]*")  # noqa: RUF001
