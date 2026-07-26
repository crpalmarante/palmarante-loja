from typing import Optional

from business_core.domain.party.party import Party, PartyType, PartyStatus
from business_core.domain.party.party_role import PartyRole, PartyRoleType, RoleStatus
from business_core.domain.party.party_address import PartyAddress, AddressType
from business_core.domain.party.party_contact import PartyContact, ContactType
from business_core.domain.party.party_document import PartyDocument
from business_core.domain.party.document import DocumentType
from business_core.domain.party.person_name import PersonName, CompanyName
from business_core.domain.party.phone_email import Phone, Email, PhoneType
from business_core.domain.party.address import Address
from business_core.shared.result import UseCaseResult, BusinessError, ErrorCategory


class CreatePartyUseCase:
    def __init__(self, party_repo):
        self._repo = party_repo

    def execute(self, command):
        errors = []

        if command.party_type == "person":
            if not command.payload.get("given_name"):
                errors.append(BusinessError(ErrorCategory.VALIDATION, "required", "given_name é obrigatório"))
            party = Party.create_person(
                given_name=command.payload.get("given_name", ""),
                family_name=command.payload.get("family_name", ""),
                display_name=command.payload.get("display_name")
            )
        elif command.payload.get("legal_name"):
            party = Party.create_organization(
                legal_name=command.payload.get("legal_name", ""),
                trade_name=command.payload.get("trade_name")
            )
        else:
            errors.append(BusinessError(ErrorCategory.VALIDATION, "required", "legal_name ou given_name obrigatório"))

        if errors:
            return UseCaseResult(success=False, errors=[vars(e) for e in errors])

        if command.payload.get("documents"):
            for doc in command.payload["documents"]:
                party.add_document(PartyDocument(
                    type=DocumentType(doc.get("type", "cpf")),
                    value=doc.get("value", ""),
                    is_main=doc.get("is_main", False)
                ))

        if command.payload.get("addresses"):
            for addr in command.payload["addresses"]:
                party.add_address(PartyAddress(
                    address=Address(
                        street=addr.get("street", ""),
                        number=addr.get("number", ""),
                        complement=addr.get("complement", ""),
                        district=addr.get("district", ""),
                        city=addr.get("city", ""),
                        region=addr.get("region", ""),
                        postal_code=addr.get("postal_code", ""),
                    ),
                    type=AddressType(addr.get("type", "main")),
                    is_main=addr.get("is_main", False)
                ))

        if command.payload.get("contacts"):
            for c in command.payload["contacts"]:
                party.add_contact(PartyContact(
                    name=c.get("name", ""),
                    phone=Phone(number=c.get("phone", "")) if c.get("phone") else None,
                    email=Email(address=c.get("email", "")) if c.get("email") else None,
                    role=c.get("role", ""),
                    is_main=c.get("is_main", False)
                ))

        if command.payload.get("roles"):
            for r in command.payload["roles"]:
                party.add_role(PartyRole(
                    role_type=PartyRoleType(r.get("type", "customer")),
                    status=RoleStatus.ACTIVE
                ))
        else:
            party.add_role(PartyRole(role_type=PartyRoleType.CUSTOMER))

        self._repo.save(party)
        events = party.clear_events()

        return UseCaseResult(success=True, data={"id": party.id, "display_name": party.display_name}, events=events)


class UpdatePartyUseCase:
    def __init__(self, party_repo):
        self._repo = party_repo

    def execute(self, command):
        party = self._repo.find_by_id(command.party_id)
        if not party:
            return UseCaseResult(success=False, errors=[{"category": "not_found", "message": "Party não encontrada"}])

        payload = command.payload or {}
        if payload.get("given_name") and party.party_type == PartyType.PERSON and party.person_name:
            name = PersonName(
                given_name=payload.get("given_name", party.person_name.given_name),
                family_name=payload.get("family_name", party.person_name.family_name),
                display_name=payload.get("display_name", party.person_name.display_name)
            )
            object.__setattr__(party, "person_name", name)

        if payload.get("legal_name") and party.party_type == PartyType.ORGANIZATION and party.company_name:
            name = CompanyName(
                legal_name=payload.get("legal_name", party.company_name.legal_name),
                trade_name=payload.get("trade_name", party.company_name.trade_name)
            )
            object.__setattr__(party, "company_name", name)

        self._repo.save(party)
        return UseCaseResult(success=True, data={"id": party.id, "display_name": party.display_name})


class ActivatePartyUseCase:
    def __init__(self, party_repo):
        self._repo = party_repo

    def execute(self, command):
        party = self._repo.find_by_id(command.party_id)
        if not party:
            return UseCaseResult(success=False, errors=[{"category": "not_found", "message": "Party não encontrada"}])
        party.activate()
        self._repo.save(party)
        return UseCaseResult(success=True, data={"id": party.id, "status": "active"}, events=party.clear_events())


class SuspendPartyUseCase:
    def __init__(self, party_repo):
        self._repo = party_repo

    def execute(self, command):
        party = self._repo.find_by_id(command.party_id)
        if not party:
            return UseCaseResult(success=False, errors=[{"category": "not_found", "message": "Party não encontrada"}])
        party.suspend()
        self._repo.save(party)
        return UseCaseResult(success=True, data={"id": party.id, "status": "suspended"}, events=party.clear_events())


class ArchivePartyUseCase:
    def __init__(self, party_repo):
        self._repo = party_repo

    def execute(self, command):
        party = self._repo.find_by_id(command.party_id)
        if not party:
            return UseCaseResult(success=False, errors=[{"category": "not_found", "message": "Party não encontrada"}])
        party.archive()
        self._repo.save(party)
        return UseCaseResult(success=True, data={"id": party.id, "status": "archived"}, events=party.clear_events())
