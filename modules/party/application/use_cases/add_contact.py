from modules.party.domain.entities.contact import Contact
from modules.party.domain.events.party_events import ContactAdded
from modules.party.domain.repositories.party_repository import PartyRepository
from modules.party.application.commands.party_commands import AddContact, RemoveContact


class AddContactUseCase:
    def __init__(self, repository: PartyRepository):
        self.repository = repository
        self.events: list = []

    def execute(self, cmd: AddContact) -> Contact:
        party = self.repository.find_by_id(cmd.party_id)
        if not party:
            raise ValueError(f'Party not found: {cmd.party_id}')

        contact = Contact(
            type=cmd.type,
            value=cmd.value,
            name=cmd.name,
            is_main=cmd.is_main
        )
        party.add_contact(contact)
        self.repository.save(party)
        self.events.append(ContactAdded(party_id=cmd.party_id, contact=contact))
        return contact

    def remove(self, cmd: RemoveContact) -> None:
        party = self.repository.find_by_id(cmd.party_id)
        if not party:
            raise ValueError(f'Party not found: {cmd.party_id}')
        party.remove_contact(cmd.contact_index)
        self.repository.save(party)
