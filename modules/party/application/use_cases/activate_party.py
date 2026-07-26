from modules.party.domain.events.party_events import PartyActivated, PartyInactivated, PartyArchived
from modules.party.domain.repositories.party_repository import PartyRepository
from modules.party.application.commands.party_commands import ActivateParty, DeactivateParty, ArchiveParty


class ActivatePartyUseCase:
    def __init__(self, repository: PartyRepository):
        self.repository = repository
        self.events: list = []

    def activate(self, cmd: ActivateParty) -> None:
        party = self.repository.find_by_id(cmd.party_id)
        if not party:
            raise ValueError(f'Party not found: {cmd.party_id}')
        party.activate()
        self.repository.save(party)
        self.events.append(PartyActivated(party_id=cmd.party_id))

    def deactivate(self, cmd: DeactivateParty) -> None:
        party = self.repository.find_by_id(cmd.party_id)
        if not party:
            raise ValueError(f'Party not found: {cmd.party_id}')
        party.deactivate()
        self.repository.save(party)
        self.events.append(PartyInactivated(party_id=cmd.party_id))

    def archive(self, cmd: ArchiveParty) -> None:
        party = self.repository.find_by_id(cmd.party_id)
        if not party:
            raise ValueError(f'Party not found: {cmd.party_id}')
        party.archive()
        self.repository.save(party)
        self.events.append(PartyArchived(party_id=cmd.party_id))
