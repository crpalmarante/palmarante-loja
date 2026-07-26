from dataclasses import dataclass


@dataclass(frozen=True)
class CorporateName:
    legal_name: str
    trade_name: str = ''

    def __str__(self) -> str:
        return self.trade_name or self.legal_name
