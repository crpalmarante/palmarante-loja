from modules.party.domain.entities.party import Party, PartyType
from modules.party.domain.entities.party_role import PartyRole
from modules.party.domain.entities.document import Document, DocumentType
from modules.party.domain.value_objects.party_id import PartyId
from modules.party.domain.value_objects.person_name import PersonName
from modules.party.domain.value_objects.corporate_name import CorporateName
from modules.party.domain.events.party_events import PartyCreated
from modules.party.domain.repositories.party_repository import PartyRepository
from modules.party.application.commands.party_commands import CreateParty


class CreatePartyUseCase:
    def __init__(self, repository: PartyRepository):
        self.repository = repository
        self.events: list = []

    def execute(self, cmd: CreateParty) -> Party:
        party_id = PartyId.generate()

        person_name = None
        corporate_name = None

        if cmd.party_type == PartyType.PERSON:
            person_name = PersonName(
                given_name=cmd.given_name,
                family_name=cmd.family_name
            )
            if not cmd.display_name:
                cmd.display_name = str(person_name)
        else:
            corporate_name = CorporateName(
                legal_name=cmd.legal_name,
                trade_name=cmd.trade_name
            )
            if not cmd.display_name:
                cmd.display_name = str(corporate_name)

        party = Party(
            id=party_id,
            party_type=cmd.party_type,
            display_name=cmd.display_name,
            person_name=person_name,
            corporate_name=corporate_name,
            notes=cmd.notes
        )

        if cmd.roles:
            for role_type in cmd.roles:
                party.assign_role(role_type)

        self.repository.save(party)
        self.events.append(PartyCreated(
            party_id=party_id,
            party_type=cmd.party_type,
            display_name=cmd.display_name
        ))
        return party
