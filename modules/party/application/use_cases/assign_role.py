from modules.party.domain.repositories.party_repository import PartyRepository
from modules.party.application.commands.party_commands import AssignRole, RemoveRole


class AssignRoleUseCase:
    def __init__(self, repository: PartyRepository):
        self.repository = repository
        self.events: list = []

    def execute(self, cmd: AssignRole) -> None:
        party = self.repository.find_by_id(cmd.party_id)
        if not party:
            raise ValueError(f'Party not found: {cmd.party_id}')
        party.assign_role(cmd.role_type)
        self.repository.save(party)

    def remove(self, cmd: RemoveRole) -> None:
        party = self.repository.find_by_id(cmd.party_id)
        if not party:
            raise ValueError(f'Party not found: {cmd.party_id}')
        party.remove_role(cmd.role_type)
        self.repository.save(party)
