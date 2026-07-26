from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class TaxRegime(str, Enum):
    SIMPLES_NACIONAL = 'simples_nacional'
    LUCRO_PRESUMIDO = 'lucro_presumido'
    LUCRO_REAL = 'lucro_real'
    MEI = 'mei'


class CRT(str, Enum):
    SN1 = 'sn1'
    SN2 = 'sn2'
    SN3 = 'sn3'
    SN4 = 'sn4'
    REGIME_NORMAL = 'regime_normal'


@dataclass
class Organization:
    party_id: str
    legal_name: str
    trade_name: str = ''
    cnpj: str = ''
    ie: str = ''
    im: str = ''
    crt: CRT = CRT.REGIME_NORMAL
    cnae: str = ''
    tax_regime: TaxRegime = TaxRegime.LUCRO_PRESUMIDO
    active: bool = True
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def deactivate(self):
        self.active = False
        self.updated_at = datetime.now()

    def activate(self):
        self.active = True
        self.updated_at = datetime.now()
