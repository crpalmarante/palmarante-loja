import os
import psycopg2
import psycopg2.extras
from datetime import datetime

from modules.party.domain.entities.party import Party, PartyType, PartyStatus
from modules.party.domain.entities.party_role import PartyRole, RoleType, RoleStatus
from modules.party.domain.entities.document import Document, DocumentType
from modules.party.domain.entities.address import Address, AddressType
from modules.party.domain.entities.contact import Contact, ContactType
from modules.party.domain.value_objects.party_id import PartyId
from modules.party.domain.value_objects.person_name import PersonName
from modules.party.domain.value_objects.corporate_name import CorporateName
from modules.party.domain.repositories.party_repository import PartyRepository


def get_connection():
    return psycopg2.connect(
        dbname=os.getenv('PG_DB', 'businesscore'),
        user=os.getenv('PG_USER', 'postgres'),
        password=os.getenv('PG_PASSWORD', 'postgres'),
        host=os.getenv('PG_HOST', 'localhost'),
        port=os.getenv('PG_PORT', '5432'),
    )


class PostgresPartyRepository(PartyRepository):

    def save(self, party: Party) -> Party:
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO party (id, party_type, display_name, given_name, family_name,
                                   legal_name, trade_name, status, notes, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (id) DO UPDATE SET
                    display_name = EXCLUDED.display_name,
                    given_name = EXCLUDED.given_name,
                    family_name = EXCLUDED.family_name,
                    legal_name = EXCLUDED.legal_name,
                    trade_name = EXCLUDED.trade_name,
                    status = EXCLUDED.status,
                    notes = EXCLUDED.notes,
                    updated_at = EXCLUDED.updated_at
            """, (
                str(party.id), party.party_type.value, party.display_name,
                party.person_name.given_name if party.person_name else '',
                party.person_name.family_name if party.person_name else '',
                party.corporate_name.legal_name if party.corporate_name else '',
                party.corporate_name.trade_name if party.corporate_name else '',
                party.status.value, party.notes,
                party.created_at, party.updated_at,
            ))

            self._save_roles(conn, party)
            self._save_documents(conn, party)
            self._save_addresses(conn, party)
            self._save_contacts(conn, party)

            conn.commit()
            return party
        finally:
            conn.close()

    def _save_roles(self, conn, party: Party):
        cur = conn.cursor()
        cur.execute('DELETE FROM party_role WHERE party_id = %s', (str(party.id),))
        for role in party.roles:
            cur.execute("""
                INSERT INTO party_role (party_id, role_type, status, created_at)
                VALUES (%s, %s, %s, %s)
            """, (str(party.id), role.role_type.value, role.status.value, role.created_at))

    def _save_documents(self, conn, party: Party):
        cur = conn.cursor()
        cur.execute('DELETE FROM party_document WHERE party_id = %s', (str(party.id),))
        for doc in party.documents:
            cur.execute("""
                INSERT INTO party_document (party_id, doc_type, doc_value, issuer, is_main, created_at)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (str(party.id), doc.type.value, doc.value, doc.issuer, doc.is_main, doc.created_at))

    def _save_addresses(self, conn, party: Party):
        cur = conn.cursor()
        cur.execute('DELETE FROM party_address WHERE party_id = %s', (str(party.id),))
        for addr in party.addresses:
            cur.execute("""
                INSERT INTO party_address (party_id, street, number, complement, district,
                    city, state, postal_code, ibge_code, country, address_type, is_main, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (str(party.id), addr.street, addr.number, addr.complement, addr.district,
                  addr.city, addr.state, addr.postal_code, addr.ibge_code, addr.country,
                  addr.address_type.value, addr.is_main, addr.created_at))

    def _save_contacts(self, conn, party: Party):
        cur = conn.cursor()
        cur.execute('DELETE FROM party_contact WHERE party_id = %s', (str(party.id),))
        for cont in party.contacts:
            cur.execute("""
                INSERT INTO party_contact (party_id, contact_type, contact_value, name, is_main, created_at)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (str(party.id), cont.type.value, cont.value, cont.name, cont.is_main, cont.created_at))

    def find_by_id(self, party_id: PartyId) -> Party | None:
        conn = get_connection()
        try:
            cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            cur.execute('SELECT * FROM party WHERE id = %s', (str(party_id),))
            row = cur.fetchone()
            if not row:
                return None
            return self._row_to_party(conn, row)
        finally:
            conn.close()

    def find_all(self, query: str = '', status: str = '', role: str = '',
                 party_type: str = '', offset: int = 0, limit: int = 50) -> list[Party]:
        conn = get_connection()
        try:
            cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            sql = 'SELECT DISTINCT p.* FROM party p'
            params = []
            wheres = []

            if query:
                wheres.append(
                    '(LOWER(p.display_name) LIKE %s OR EXISTS (SELECT 1 FROM party_document pd WHERE pd.party_id = p.id AND LOWER(pd.doc_value) LIKE %s))'
                )
                params.extend([f'%{query.lower()}%', f'%{query.lower()}%'])

            if status:
                wheres.append('p.status = %s')
                params.append(status)

            if party_type:
                wheres.append('p.party_type = %s')
                params.append(party_type)

            if role:
                wheres.append('EXISTS (SELECT 1 FROM party_role pr WHERE pr.party_id = p.id AND pr.role_type = %s AND pr.status = %s)')
                params.extend([role, 'active'])

            if wheres:
                sql += ' WHERE ' + ' AND '.join(wheres)

            sql += ' ORDER BY p.created_at DESC LIMIT %s OFFSET %s'
            params.extend([limit, offset])

            cur.execute(sql, params)
            rows = cur.fetchall()
            return [self._row_to_party(conn, row) for row in rows]
        finally:
            conn.close()

    def count(self, query: str = '', status: str = '', role: str = '',
              party_type: str = '') -> int:
        conn = get_connection()
        try:
            cur = conn.cursor()
            sql = 'SELECT COUNT(DISTINCT p.id) FROM party p'
            params = []
            wheres = []

            if query:
                wheres.append(
                    '(LOWER(p.display_name) LIKE %s OR EXISTS (SELECT 1 FROM party_document pd WHERE pd.party_id = p.id AND LOWER(pd.doc_value) LIKE %s))'
                )
                params.extend([f'%{query.lower()}%', f'%{query.lower()}%'])

            if status:
                wheres.append('p.status = %s')
                params.append(status)

            if party_type:
                wheres.append('p.party_type = %s')
                params.append(party_type)

            if role:
                wheres.append('EXISTS (SELECT 1 FROM party_role pr WHERE pr.party_id = p.id AND pr.role_type = %s AND pr.status = %s)')
                params.extend([role, 'active'])

            if wheres:
                sql += ' WHERE ' + ' AND '.join(wheres)

            cur.execute(sql, params)
            return cur.fetchone()[0]
        finally:
            conn.close()

    def delete(self, party_id: PartyId) -> None:
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute('DELETE FROM party WHERE id = %s', (str(party_id),))
            conn.commit()
        finally:
            conn.close()

    def _row_to_party(self, conn, row) -> Party:
        party = Party(
            id=PartyId.from_string(str(row['id'])),
            party_type=PartyType(row['party_type']),
            display_name=row['display_name'],
            person_name=PersonName(
                given_name=row.get('given_name') or '',
                family_name=row.get('family_name') or '',
            ) if row['party_type'] == 'person' else None,
            corporate_name=CorporateName(
                legal_name=row.get('legal_name') or '',
                trade_name=row.get('trade_name') or '',
            ) if row['party_type'] == 'company' else None,
            status=PartyStatus(row['status']),
            notes=row.get('notes') or '',
            created_at=row['created_at'],
            updated_at=row['updated_at'],
        )

        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        cur.execute('SELECT * FROM party_role WHERE party_id = %s', (str(row['id']),))
        for r in cur.fetchall():
            party.roles.append(PartyRole(
                role_type=RoleType(r['role_type']),
                status=RoleStatus(r['status']),
                created_at=r['created_at'],
            ))

        cur.execute('SELECT * FROM party_document WHERE party_id = %s', (str(row['id']),))
        for d in cur.fetchall():
            party.documents.append(Document(
                type=DocumentType(d['doc_type']),
                value=d['doc_value'],
                issuer=d.get('issuer') or '',
                is_main=d['is_main'],
                created_at=d['created_at'],
            ))

        cur.execute('SELECT * FROM party_address WHERE party_id = %s', (str(row['id']),))
        for a in cur.fetchall():
            party.addresses.append(Address(
                street=a.get('street') or '',
                number=a.get('number') or '',
                complement=a.get('complement') or '',
                district=a.get('district') or '',
                city=a.get('city') or '',
                state=a.get('state') or '',
                postal_code=a.get('postal_code') or '',
                ibge_code=a.get('ibge_code') or '',
                country=a.get('country') or 'Brasil',
                address_type=AddressType(a['address_type']),
                is_main=a['is_main'],
                created_at=a['created_at'],
            ))

        cur.execute('SELECT * FROM party_contact WHERE party_id = %s', (str(row['id']),))
        for c in cur.fetchall():
            party.contacts.append(Contact(
                type=ContactType(c['contact_type']),
                value=c['contact_value'],
                name=c.get('name') or '',
                is_main=c['is_main'],
                created_at=c['created_at'],
            ))

        return party
