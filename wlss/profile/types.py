from __future__ import annotations

import re

from wlss.core.types import PositiveInt, Str


class ProfileDescription(Str):
    LENGTH_MAX = PositiveInt(1000)
    LENGTH_MIN = PositiveInt(1)
    REGEXP = re.compile(r".{1,1000}", flags=re.DOTALL)


class ProfileName(Str):
    LENGTH_MAX = PositiveInt(50)
    LENGTH_MIN = PositiveInt(1)
    REGEXP = re.compile(r"[A-Za-zА-яЁё'-.() ]*")  # noqa: RUF001
