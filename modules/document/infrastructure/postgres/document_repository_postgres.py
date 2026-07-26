from datetime import datetime
from modules.document.domain.entities.business_document import (
    BusinessDocument, DocumentHeader, DocumentLine, DocumentParty,
    DocumentReference, DocumentHistory,
)
from modules.document.domain.entities.document_definition import DocumentDefinition, DocumentFieldDef, DocumentLineFieldDef, FieldType
from modules.document.domain.entities.document_numbering import DocumentNumbering
from modules.document.domain.value_objects.document_status import DocumentStatus
from modules.document.domain.repositories.document_repository import DocumentRepository


class DocumentRepositoryMemory(DocumentRepository):
    _counter = 0

    def __init__(self):
        self._documents = {}
        self._definitions = {}
        self._numbering = {}

    def _next_id(self) -> str:
        self.__class__._counter += 1
        return str(self.__class__._counter)

    def delete_document(self, doc_id: str) -> None:
        self._documents.pop(doc_id, None)

    def save_document(self, doc: BusinessDocument) -> BusinessDocument:
        if not doc._id:
            doc._id = self._next_id()
        self._documents[doc._id] = doc
        for i, l in enumerate(doc.lines):
            if not l._id:
                l._id = f'{doc._id}_l{i}'
            l.document_id = doc._id
        for p in doc.parties:
            if not p._id:
                p._id = self._next_id()
            p.document_id = doc._id
        return doc

    def find_document_by_id(self, doc_id: str) -> BusinessDocument | None:
        return self._documents.get(doc_id)

    def find_documents(self, document_type: str = '', status: str = '',
                       party_id: str = '', query: str = '',
                       limit: int = 100) -> list[BusinessDocument]:
        results = list(self._documents.values())
        if document_type:
            results = [d for d in results if d.document_type == document_type]
        if status:
            results = [d for d in results if d.status.value == status]
        if party_id:
            results = [d for d in results if any(p.party_id == party_id for p in d.parties)]
        if query:
            q = query.lower()
            results = [d for d in results if q in d.number.lower() or q in (d.header.notes or '').lower()]
        results.sort(key=lambda d: d.created_at, reverse=True)
        return results[:limit]

    def find_documents_by_reference(self, reference_type: str, reference_id: str) -> list[BusinessDocument]:
        return [d for d in self._documents.values() if any(
            r.reference_type == reference_type and r.reference_id == reference_id
            for r in d.references
        )]

    def save_definition(self, defn: DocumentDefinition) -> DocumentDefinition:
        if not defn._id:
            defn._id = self._next_id()
        self._definitions[defn._id] = defn
        return defn

    def find_definition_by_id(self, def_id: str) -> DocumentDefinition | None:
        return self._definitions.get(def_id)

    def find_definition_by_code(self, code: str) -> DocumentDefinition | None:
        for d in self._definitions.values():
            if d.code == code:
                return d
        return None

    def find_all_definitions(self, active: bool = True) -> list[DocumentDefinition]:
        return [d for d in self._definitions.values() if d.active == active]

    def save_numbering(self, numbering: DocumentNumbering) -> DocumentNumbering:
        if not numbering._id:
            numbering._id = self._next_id()
        self._numbering[numbering._id] = numbering
        return numbering

    def find_numbering(self, document_type: str, series: str = '') -> DocumentNumbering | None:
        for n in self._numbering.values():
            if n.document_type == document_type and (not series or n.series == series):
                return n
        return None

    def find_all_numbering(self) -> list[DocumentNumbering]:
        return list(self._numbering.values())
