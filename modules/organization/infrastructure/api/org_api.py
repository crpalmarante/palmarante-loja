import uvicorn
from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from modules.organization.infrastructure.postgres.memory_repository import InMemoryOrganizationRepository
from modules.organization.domain.entities.organization import TaxRegime, CRT
from modules.organization.application.commands.org_commands import (
    CreateOrganization, UpdateOrganization, CreateBranch,
)
from modules.organization.application.use_cases.create_organization import CreateOrganizationUseCase

app = FastAPI(title='BusinessCore — Organization Module', version='1.0.0')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

repo = InMemoryOrganizationRepository()
create_uc = CreateOrganizationUseCase(repo)


def org_to_dict(o):
    return {
        'id': o.party_id,
        'party_id': o.party_id,
        'legal_name': o.legal_name,
        'trade_name': o.trade_name,
        'cnpj': o.cnpj,
        'ie': o.ie,
        'im': o.im,
        'crt': o.crt.value,
        'cnae': o.cnae,
        'tax_regime': o.tax_regime.value,
        'active': o.active,
        'created_at': o.created_at.isoformat(),
        'updated_at': o.updated_at.isoformat(),
    }


def branch_to_dict(b):
    return {
        'organization_id': b.organization_id,
        'party_id': b.party_id,
        'code': b.code,
        'name': b.name,
        'cnpj': b.cnpj,
        'ie': b.ie,
        'phone': b.phone,
        'email': b.email,
        'active': b.active,
    }


@app.get('/api/organizations')
def list_orgs(query: str = Query(''), active: bool | None = None):
    orgs = repo.find_all_organizations(query, active)
    return {'data': [org_to_dict(o) for o in orgs], 'total': len(orgs)}


@app.get('/api/organizations/{org_id}')
def get_org(org_id: str):
    org = repo.find_organization_by_id(org_id)
    if not org:
        raise HTTPException(404, 'Organization not found')
    return {'data': org_to_dict(org)}


@app.post('/api/organizations')
def create_org(body: dict):
    cmd = CreateOrganization(
        party_id=body.get('party_id', ''),
        legal_name=body.get('legal_name', ''),
        trade_name=body.get('trade_name', ''),
        cnpj=body.get('cnpj', ''),
        ie=body.get('ie', ''),
        im=body.get('im', ''),
        crt=CRT(body.get('crt', 'regime_normal')),
        cnae=body.get('cnae', ''),
        tax_regime=TaxRegime(body.get('tax_regime', 'lucro_presumido')),
    )
    org = create_uc.execute(cmd)
    return {'data': org_to_dict(org)}


@app.put('/api/organizations/{org_id}')
def update_org(org_id: str, body: dict):
    org = repo.find_organization_by_id(org_id)
    if not org:
        raise HTTPException(404, 'Organization not found')

    if 'trade_name' in body:
        org.trade_name = body['trade_name']
    if 'ie' in body:
        org.ie = body['ie']
    if 'im' in body:
        org.im = body['im']
    if 'crt' in body:
        org.crt = CRT(body['crt'])
    if 'cnae' in body:
        org.cnae = body['cnae']
    if 'tax_regime' in body:
        org.tax_regime = TaxRegime(body['tax_regime'])
    if 'active' in body:
        org.active = body['active']

    org.updated_at = __import__('datetime').datetime.now()
    repo.save_organization(org)
    return {'data': org_to_dict(org)}


@app.get('/api/organizations/{org_id}/branches')
def list_branches(org_id: str):
    branches = repo.find_branches_by_organization(org_id)
    return {'data': [branch_to_dict(b) for b in branches]}


@app.post('/api/organizations/{org_id}/branches')
def create_branch(org_id: str, body: dict):
    from modules.organization.application.commands.org_commands import CreateBranch
    from modules.organization.domain.entities.branch import Branch
    branch = Branch(
        organization_id=org_id,
        party_id=body.get('party_id', ''),
        code=body.get('code', ''),
        name=body.get('name', ''),
        cnpj=body.get('cnpj', ''),
        ie=body.get('ie', ''),
        phone=body.get('phone', ''),
        email=body.get('email', ''),
    )
    repo.save_branch(branch)
    return {'data': branch_to_dict(branch)}


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8002)
