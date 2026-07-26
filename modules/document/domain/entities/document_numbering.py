from dataclasses import dataclass
from datetime import datetime


@dataclass
class DocumentNumbering:
    document_type: str
    code: str = ''
    name: str = ''
    pattern: str = '{year}{month}{seq:06d}'
    prefix: str = ''
    suffix: str = ''
    next_number: int = 1
    digits: int = 6
    series: str = '1'
    active: bool = True
    created_at: datetime = None
    _id: str = ''

    def __post_init__(self):
        if self.code == '':
            self.code = self.document_type
        if self.name == '':
            self.name = self.document_type.replace('_', ' ').title()
        if self.created_at is None:
            self.created_at = datetime.now()

    def generate_number(self) -> str:
        import re
        from datetime import date
        today = date.today()
        seq = str(self.next_number).zfill(self.digits)
        result = self.pattern
        result = result.replace('{year}', str(today.year))
        result = result.replace('{month}', str(today.month).zfill(2))
        result = result.replace('{day}', str(today.day).zfill(2))
        result = re.sub(r'\{seq(?::\d+d)?\}', seq, result)
        result = result.replace('{series}', self.series)
        if self.prefix:
            result = self.prefix + result
        if self.suffix:
            result = result + self.suffix
        return result

    def advance(self):
        self.next_number += 1
