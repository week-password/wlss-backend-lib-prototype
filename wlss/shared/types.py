from __future__ import annotations

from datetime import timezone

from wlss.core.types import AwareDatetime, PositiveInt


class Id(PositiveInt):
    ...


class UtcDatetime(AwareDatetime):
    TIMEZONE = timezone.utc
