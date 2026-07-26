from dataclasses import dataclass
from modules.organization.domain.entities.organization import TaxRegime, CRT


@dataclass
class CreateOrganization:
    party_id: str
    legal_name: str
    trade_name: str = ''
    cnpj: str = ''
    ie: str = ''
    im: str = ''
    crt: CRT = CRT.REGIME_NORMAL
    cnae: str = ''
    tax_regime: TaxRegime = TaxRegime.LUCRO_PRESUMIDO


@dataclass
class UpdateOrganization:
    org_id: str
    trade_name: str | None = None
    ie: str | None = None
    im: str | None = None
    crt: CRT | None = None
    cnae: str | None = None
    tax_regime: TaxRegime | None = None
    active: bool | None = None


@dataclass
class CreateBranch:
    organization_id: str
    party_id: str
    code: str = ''
    name: str = ''
    cnpj: str = ''
    ie: str = ''
    phone: str = ''
    email: str = ''
