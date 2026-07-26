import os
import uvicorn
from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from modules.party.domain.entities.party import PartyType
from modules.party.domain.entities.party_role import RoleType
from modules.party.domain.entities.document import DocumentType
from modules.party.domain.entities.address import AddressType
from modules.party.domain.entities.contact import ContactType
from modules.party.domain.value_objects.party_id import PartyId
from modules.party.infrastructure.postgres.memory_repository import InMemoryPartyRepository
from modules.party.infrastructure.postgres.postgres_repository import PostgresPartyRepository
from modules.party.application.commands.party_commands import (
    CreateParty, UpdateParty, ActivateParty, DeactivateParty, ArchiveParty,
    AssignRole, RemoveRole, AddDocument, RemoveDocument, AddAddress, RemoveAddress,
    AddContact, RemoveContact
)
from modules.party.application.use_cases.create_party import CreatePartyUseCase
from modules.party.application.use_cases.update_party import UpdatePartyUseCase
from modules.party.application.use_cases.assign_role import AssignRoleUseCase
from modules.party.application.use_cases.add_document import AddDocumentUseCase
from modules.party.application.use_cases.add_address import AddAddressUseCase
from modules.party.application.use_cases.add_contact import AddContactUseCase
from modules.party.application.use_cases.activate_party import ActivatePartyUseCase

app = FastAPI(title='BusinessCore — Party Module', version='1.0.0')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

if os.getenv('PG_HOST'):
    repo = PostgresPartyRepository()
else:
    repo = InMemoryPartyRepository()

create_party_uc = CreatePartyUseCase(repo)
update_party_uc = UpdatePartyUseCase(repo)
assign_role_uc = AssignRoleUseCase(repo)
add_document_uc = AddDocumentUseCase(repo)
add_address_uc = AddAddressUseCase(repo)
add_contact_uc = AddContactUseCase(repo)
activate_party_uc = ActivatePartyUseCase(repo)


def party_to_dict(party):
    return {
        'id': str(party.id),
        'party_type': party.party_type.value,
        'display_name': party.display_name,
        'given_name': party.person_name.given_name if party.person_name else '',
        'family_name': party.person_name.family_name if party.person_name else '',
        'legal_name': party.corporate_name.legal_name if party.corporate_name else '',
        'trade_name': party.corporate_name.trade_name if party.corporate_name else '',
        'status': party.status.value,
        'notes': party.notes,
        'roles': [{'role_type': r.role_type.value, 'status': r.status.value} for r in party.roles],
        'documents': [{'type': d.type.value, 'value': d.value, 'issuer': d.issuer, 'is_main': d.is_main} for d in party.documents],
        'addresses': [{
            'street': a.street, 'number': a.number, 'complement': a.complement,
            'district': a.district, 'city': a.city, 'state': a.state,
            'postal_code': a.postal_code, 'ibge_code': a.ibge_code,
            'country': a.country, 'address_type': a.address_type.value, 'is_main': a.is_main
        } for a in party.addresses],
        'contacts': [{'type': c.type.value, 'value': c.value, 'name': c.name, 'is_main': c.is_main} for c in party.contacts],
        'created_at': party.created_at.isoformat(),
        'updated_at': party.updated_at.isoformat(),
    }


@app.get('/api/parties')
def list_parties(
    query: str = Query(''),
    status: str = Query(''),
    role: str = Query(''),
    party_type: str = Query(''),
    offset: int = Query(0),
    limit: int = Query(50),
):
    parties = repo.find_all(query, status, role, party_type, offset, limit)
    total = repo.count(query, status, role, party_type)
    return {
        'data': [party_to_dict(p) for p in parties],
        'total': total,
        'offset': offset,
        'limit': limit,
    }


@app.get('/api/parties/{party_id}')
def get_party(party_id: str):
    party = repo.find_by_id(PartyId.from_string(party_id))
    if not party:
        raise HTTPException(404, 'Party not found')
    return {'data': party_to_dict(party)}


@app.post('/api/parties')
def create_party(body: dict):
    cmd = CreateParty(
        party_type=PartyType(body.get('party_type', 'person')),
        display_name=body.get('display_name', ''),
        given_name=body.get('given_name', ''),
        family_name=body.get('family_name', ''),
        legal_name=body.get('legal_name', ''),
        trade_name=body.get('trade_name', ''),
        notes=body.get('notes', ''),
        roles=[RoleType(r['type']) for r in body.get('roles', [])] if body.get('roles') else None,
    )
    party = create_party_uc.execute(cmd)

    # Add document if provided
    for doc in body.get('documents', []):
        add_document_uc.execute(AddDocument(
            party_id=party.id,
            type=DocumentType(doc.get('type', 'other')),
            value=doc.get('value', ''),
            issuer=doc.get('issuer', ''),
            is_main=doc.get('is_main', False),
        ))

    # Add addresses if provided
    for addr in body.get('addresses', []):
        add_address_uc.execute(AddAddress(
            party_id=party.id,
            street=addr.get('street', ''),
            number=addr.get('number', ''),
            complement=addr.get('complement', ''),
            district=addr.get('district', ''),
            city=addr.get('city', ''),
            state=addr.get('state', ''),
            postal_code=addr.get('postal_code', ''),
            ibge_code=addr.get('ibge_code', ''),
            country=addr.get('country', 'Brasil'),
            is_main=addr.get('is_main', False),
        ))

    # Add contacts if provided
    for cont in body.get('contacts', []):
        add_contact_uc.execute(AddContact(
            party_id=party.id,
            type=ContactType(cont.get('type', 'other')),
            value=cont.get('value', ''),
            name=cont.get('name', ''),
            is_main=cont.get('is_main', False),
        ))

    return {'data': party_to_dict(repo.find_by_id(party.id))}


@app.put('/api/parties/{party_id}')
def update_party(party_id: str, body: dict):
    cmd = UpdateParty(
        party_id=PartyId.from_string(party_id),
        display_name=body.get('display_name'),
        given_name=body.get('given_name'),
        family_name=body.get('family_name'),
        legal_name=body.get('legal_name'),
        trade_name=body.get('trade_name'),
        notes=body.get('notes'),
    )
    party = update_party_uc.execute(cmd)

    # Update roles
    if 'roles' in body:
        all_role_types = [r.role_type for r in party.roles]
        for r_data in body['roles']:
            rt = RoleType(r_data['type'])
            if rt not in all_role_types:
                assign_role_uc.execute(AssignRole(party_id=PartyId.from_string(party_id), role_type=rt))

    # Update documents
    if 'documents' in body:
        party.documents = []
        for doc in body['documents']:
            add_document_uc.execute(AddDocument(
                party_id=party.id,
                type=DocumentType(doc.get('type', 'other')),
                value=doc.get('value', ''),
                issuer=doc.get('issuer', ''),
                is_main=doc.get('is_main', False),
            ))

    # Update addresses
    if 'addresses' in body:
        party.addresses = []
        for addr in body['addresses']:
            add_address_uc.execute(AddAddress(
                party_id=party.id,
                street=addr.get('street', ''),
                number=addr.get('number', ''),
                complement=addr.get('complement', ''),
                district=addr.get('district', ''),
                city=addr.get('city', ''),
                state=addr.get('state', ''),
                postal_code=addr.get('postal_code', ''),
                ibge_code=addr.get('ibge_code', ''),
                country=addr.get('country', 'Brasil'),
                is_main=addr.get('is_main', False),
            ))

    # Update contacts
    if 'contacts' in body:
        party.contacts = []
        for cont in body['contacts']:
            add_contact_uc.execute(AddContact(
                party_id=party.id,
                type=ContactType(cont.get('type', 'other')),
                value=cont.get('value', ''),
                name=cont.get('name', ''),
                is_main=cont.get('is_main', False),
            ))

    return {'data': party_to_dict(repo.find_by_id(party.id))}


@app.post('/api/parties/{party_id}/activate')
def activate_party(party_id: str):
    activate_party_uc.activate(ActivateParty(party_id=PartyId.from_string(party_id)))
    return {'status': 'ok'}


@app.post('/api/parties/{party_id}/deactivate')
def deactivate_party(party_id: str):
    activate_party_uc.deactivate(DeactivateParty(party_id=PartyId.from_string(party_id)))
    return {'status': 'ok'}


@app.post('/api/parties/{party_id}/archive')
def archive_party(party_id: str):
    activate_party_uc.archive(ArchiveParty(party_id=PartyId.from_string(party_id)))
    return {'status': 'ok'}


@app.delete('/api/parties/{party_id}')
def delete_party(party_id: str):
    repo.delete(PartyId.from_string(party_id))
    return {'status': 'ok'}


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
