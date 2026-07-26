from modules.party.domain.entities.document import Document
from modules.party.domain.events.party_events import DocumentAdded
from modules.party.domain.repositories.party_repository import PartyRepository
from modules.party.application.commands.party_commands import AddDocument, RemoveDocument


class AddDocumentUseCase:
    def __init__(self, repository: PartyRepository):
        self.repository = repository
        self.events: list = []

    def execute(self, cmd: AddDocument) -> Document:
        party = self.repository.find_by_id(cmd.party_id)
        if not party:
            raise ValueError(f'Party not found: {cmd.party_id}')

        doc = Document(
            type=cmd.type,
            value=cmd.value,
            issuer=cmd.issuer,
            is_main=cmd.is_main
        )
        party.add_document(doc)
        self.repository.save(party)
        self.events.append(DocumentAdded(party_id=cmd.party_id, document=doc))
        return doc

    def remove(self, cmd: RemoveDocument) -> None:
        party = self.repository.find_by_id(cmd.party_id)
        if not party:
            raise ValueError(f'Party not found: {cmd.party_id}')
        party.remove_document(cmd.document_index)
        self.repository.save(party)
