from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class DateRange:
    start: date
    end: date | None = None

    def is_active(self) -> bool:
        today = date.today()
        if self.end:
            return self.start <= today <= self.end
        return self.start <= today

    def __str__(self) -> str:
        if self.end:
            return f'{self.start.isoformat()} a {self.end.isoformat()}'
        return f'desde {self.start.isoformat()}'
