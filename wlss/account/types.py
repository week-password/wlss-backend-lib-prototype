from __future__ import annotations

import re

from wlss.core.types import PositiveInt, Str


class AccountEmail(Str):
    LENGTH_MAX = PositiveInt(200)
    LENGTH_MIN = PositiveInt(5)
    REGEXP = re.compile(r".+@.+\..+")


class AccountLogin(Str):
    LENGTH_MAX = PositiveInt(50)
    LENGTH_MIN = PositiveInt(1)
    REGEXP = re.compile(r"[A-Za-z0-9\-_]*")


class AccountPassword(Str):
    LENGTH_MIN = PositiveInt(8)
    LENGTH_MAX = PositiveInt(500)
