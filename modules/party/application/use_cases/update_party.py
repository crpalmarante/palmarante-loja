from modules.party.domain.entities.party import Party, PartyStatus
from modules.party.domain.value_objects.person_name import PersonName
from modules.party.domain.value_objects.corporate_name import CorporateName
from modules.party.domain.events.party_events import PartyUpdated
from modules.party.domain.repositories.party_repository import PartyRepository
from modules.party.application.commands.party_commands import UpdateParty


class UpdatePartyUseCase:
    def __init__(self, repository: PartyRepository):
        self.repository = repository
        self.events: list = []

    def execute(self, cmd: UpdateParty) -> Party:
        party = self.repository.find_by_id(cmd.party_id)
        if not party:
            raise ValueError(f'Party not found: {cmd.party_id}')

        if cmd.display_name is not None:
            party.display_name = cmd.display_name
        if cmd.given_name is not None or cmd.family_name is not None:
            given = cmd.given_name if cmd.given_name is not None else (party.person_name.given_name if party.person_name else '')
            family = cmd.family_name if cmd.family_name is not None else (party.person_name.family_name if party.person_name else '')
            party.person_name = PersonName(given_name=given, family_name=family)
        if cmd.legal_name is not None or cmd.trade_name is not None:
            legal = cmd.legal_name if cmd.legal_name is not None else (party.corporate_name.legal_name if party.corporate_name else '')
            trade = cmd.trade_name if cmd.trade_name is not None else (party.corporate_name.trade_name if party.corporate_name else '')
            party.corporate_name = CorporateName(legal_name=legal, trade_name=trade)
        if cmd.notes is not None:
            party.notes = cmd.notes

        self.repository.save(party)
        self.events.append(PartyUpdated(party_id=cmd.party_id))
        return party
