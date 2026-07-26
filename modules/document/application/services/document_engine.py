from datetime import datetime
from modules.document.domain.entities.business_document import (
    BusinessDocument, DocumentHeader, DocumentLine, DocumentParty,
    DocumentReference, DocumentHistory,
)
from modules.document.domain.entities.document_definition import DocumentDefinition
from modules.document.domain.entities.document_numbering import DocumentNumbering
from modules.document.domain.value_objects.document_status import DocumentStatus
from modules.document.domain.repositories.document_repository import DocumentRepository


class DocumentEngine:
    def __init__(self, repo: DocumentRepository):
        self._repo = repo

    def create_document(self, doc_type: str, number: str = '',
                        organization_id: str = '', branch_id: str = '',
                        direction: str = 'out', header: dict = None,
                        lines: list = None, parties: list = None,
                        references: list = None, notes: str = '',
                        freight: float = 0.0, insurance: float = 0.0,
                        other_costs: float = 0.0,
                        created_by: str = '') -> BusinessDocument:
        definition = self._repo.find_definition_by_code(doc_type)
        if not definition:
            raise ValueError(f'Document definition "{doc_type}" not found')

        doc_number = number
        if not doc_number:
            numbering = self._repo.find_numbering(doc_type)
            if numbering:
                doc_number = numbering.generate_number()
                numbering.advance()
                self._repo.save_numbering(numbering)

        doc = BusinessDocument(
            document_type=doc_type,
            definition_id=definition._id,
            number=doc_number,
            header=DocumentHeader(**(header or {}), notes=notes),
            organization_id=organization_id,
            branch_id=branch_id,
            direction=direction or definition.direction,
            freight=freight, insurance=insurance, other_costs=other_costs,
            created_by=created_by,
        )

        for l in (lines or []):
            doc.add_line(DocumentLine(**l))
        for p in (parties or []):
            if isinstance(p, dict):
                p = DocumentParty(**p)
            doc.add_party(p)

        doc = self._repo.save_document(doc)

        for r in (references or []):
            if isinstance(r, dict):
                r['document_id'] = doc._id
                r = DocumentReference(**r)
            else:
                r.document_id = doc._id
            doc.add_reference(r)

        if references:
            doc = self._repo.save_document(doc)

        doc.recalc_totals()
        doc.add_history('created', to_status=doc.status.value, performed_by=created_by)
        return self._repo.save_document(doc)

    def change_status(self, doc_id: str, new_status: str,
                      comment: str = '', performed_by: str = '') -> BusinessDocument:
        doc = self._repo.find_document_by_id(doc_id)
        if not doc:
            raise ValueError(f'Document {doc_id} not found')
        status = DocumentStatus(new_status)
        doc.change_status(status, comment=comment, performed_by=performed_by)
        return self._repo.save_document(doc)

    def add_line(self, doc_id: str, line_data: dict) -> BusinessDocument:
        doc = self._repo.find_document_by_id(doc_id)
        if not doc:
            raise ValueError(f'Document {doc_id} not found')
        doc.add_line(DocumentLine(**line_data))
        return self._repo.save_document(doc)

    def remove_line(self, doc_id: str, line_id: str) -> BusinessDocument:
        doc = self._repo.find_document_by_id(doc_id)
        if not doc:
            raise ValueError(f'Document {doc_id} not found')
        doc.lines = [l for l in doc.lines if (l._id or '') != line_id]
        doc.recalc_totals()
        return self._repo.save_document(doc)

    def register_definition(self, name: str, code: str, **kwargs) -> DocumentDefinition:
        existing = self._repo.find_definition_by_code(code)
        if existing:
            raise ValueError(f'Definition "{code}" already exists')
        defn = DocumentDefinition(name=name, code=code, **kwargs)
        for bh in defn.behaviors:
            if isinstance(bh, str):
                from modules.document.domain.entities.document_definition import BehaviorType
                pass
        return self._repo.save_definition(defn)

    def setup_numbering(self, doc_type: str, pattern: str = '{year}{month}{seq:06d}',
                        prefix: str = '', suffix: str = '', digits: int = 6,
                        series: str = '1', next_number: int = 1) -> DocumentNumbering:
        num = DocumentNumbering(
            document_type=doc_type, pattern=pattern, prefix=prefix,
            suffix=suffix, digits=digits, series=series, next_number=next_number,
        )
        return self._repo.save_numbering(num)

    def get_dashboard(self) -> dict:
        all_docs = self._repo.find_documents()
        by_type = {}
        by_status = {}
        total_value = 0.0
        for d in all_docs:
            by_type[d.document_type] = by_type.get(d.document_type, 0) + 1
            by_status[d.status.value] = by_status.get(d.status.value, 0) + 1
            total_value += d.total
        definitions = self._repo.find_all_definitions()
        return {
            'total_documents': len(all_docs),
            'total_value': round(total_value, 2),
            'active_definitions': len(definitions),
            'by_type': by_type,
            'by_status': by_status,
        }
