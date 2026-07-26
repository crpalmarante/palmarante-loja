#!/usr/bin/env python3
"""BusinessCore Party API — servidor de desenvolvimento."""
import http.server
import json
import os
import sys
import uuid
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from business_core.commands.party.party_commands import CreateParty, ActivateParty, SuspendParty, ArchiveParty
from business_core.use_cases.party.party_use_cases import (
    CreatePartyUseCase, UpdatePartyUseCase,
    ActivatePartyUseCase, SuspendPartyUseCase, ArchivePartyUseCase
)

PORT = 8081
FRONTEND_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "frontend")


class InMemoryPartyRepo:
    def __init__(self):
        self._store = {}

    def save(self, party):
        self._store[party.id] = party

    def find_by_id(self, party_id):
        return self._store.get(party_id)

    def find_by_document(self, value):
        for p in self._store.values():
            for d in p.documents:
                if d.value == value:
                    return p
        return None

    def list(self, status="", role="", query="", party_type="", offset=0, limit=50):
        result = list(self._store.values())
        if status:
            result = [p for p in result if p.status.value == status]
        if role:
            result = [p for p in result if p.has_role(role)]
        if party_type:
            result = [p for p in result if p.party_type.value == party_type]
        if query:
            q = query.lower()
            result = [p for p in result if q in p.display_name.lower()]
        result.sort(key=lambda p: p.created_at, reverse=True)
        return result[offset:offset + limit]

    def count(self, status="", role="", query=""):
        return len(self.list(status, role, query))

    def delete(self, party_id):
        if party_id in self._store:
            del self._store[party_id]

    def exists_by_document(self, value):
        return self.find_by_document(value) is not None


party_repo = InMemoryPartyRepo()


def party_to_dict(p):
    return {
        "id": p.id,
        "party_type": p.party_type.value,
        "display_name": p.display_name,
        "status": p.status.value,
        "person_name": {
            "given_name": p.person_name.given_name,
            "family_name": p.person_name.family_name,
            "display_name": p.person_name.display_name
        } if p.person_name else None,
        "company_name": {
            "legal_name": p.company_name.legal_name,
            "trade_name": p.company_name.trade_name
        } if p.company_name else None,
        "documents": [{"type": d.type.value, "value": d.value, "is_main": d.is_main} for d in p.documents],
        "roles": [{"role_type": r.role_type.value, "status": r.status.value} for r in p.roles],
        "addresses": [{
            "address": {
                "street": a.address.street,
                "number": a.address.number,
                "complement": a.address.complement,
                "district": a.address.district,
                "city": a.address.city,
                "region": a.address.region,
                "postal_code": a.address.postal_code,
                "country": a.address.country
            },
            "type": a.type.value,
            "is_main": a.is_main
        } for a in p.addresses],
        "contacts": [{
            "name": c.name,
            "phone": str(c.phone) if c.phone else "",
            "email": str(c.email) if c.email else "",
            "is_main": c.is_main
        } for c in p.contacts],
        "created_at": p.created_at.isoformat() if p.created_at else "",
        "updated_at": p.updated_at.isoformat() if p.updated_at else ""
    }


class PartyAPIHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path.rstrip("/")

        # Serve frontend files
        if path == "/" or not path.startswith("/api"):
            self.directory = FRONTEND_DIR
            if path == "/":
                self.path = "/index.html"
            elif path.startswith("/pages/"):
                self.directory = os.path.join(FRONTEND_DIR, "pages")
            return super().do_GET()

        # API routes
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()

        if path == "/api/parties":
            params = urllib.parse.parse_qs(parsed.query)
            status = params.get("status", [""])[0]
            role = params.get("role", [""])[0]
            query = params.get("query", [""])[0]
            party_type = params.get("party_type", [""])[0]
            parties = party_repo.list(status=status, role=role, query=query, party_type=party_type)
            data = [party_to_dict(p) for p in parties]
            self.wfile.write(json.dumps({"success": True, "data": data, "total": len(data)}).encode())

        elif path.startswith("/api/parties/"):
            party_id = path.split("/")[-1]
            if party_id in ("activate", "suspend", "archive"):
                self.wfile.write(json.dumps({"success": False, "error": "missing id"}).encode())
                return
            p = party_repo.find_by_id(party_id)
            if not p:
                self.wfile.write(json.dumps({"success": False, "error": "not found"}).encode())
            else:
                self.wfile.write(json.dumps({"success": True, "data": party_to_dict(p)}).encode())

    def do_POST(self):
        content_len = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(content_len)) if content_len else {}
        path = self.path.rstrip("/")

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()

        if path == "/api/parties":
            cmd = CreateParty(party_type=body.get("party_type", "person"), payload=body)
            result = CreatePartyUseCase(party_repo).execute(cmd)
            self.wfile.write(json.dumps({
                "success": result.success,
                "data": result.data,
                "errors": result.errors
            }).encode())

        elif path.startswith("/api/parties/") and path.endswith("/activate"):
            party_id = path.split("/")[-2]
            cmd = type("ActivateParty", (), {"party_id": party_id})()
            result = ActivatePartyUseCase(party_repo).execute(cmd)
            self.wfile.write(json.dumps({"success": result.success, "data": result.data}).encode())

        elif path.startswith("/api/parties/") and path.endswith("/suspend"):
            party_id = path.split("/")[-2]
            cmd = type("SuspendParty", (), {"party_id": party_id})()
            result = SuspendPartyUseCase(party_repo).execute(cmd)
            self.wfile.write(json.dumps({"success": result.success, "data": result.data}).encode())

        elif path.startswith("/api/parties/") and path.endswith("/archive"):
            party_id = path.split("/")[-2]
            cmd = type("ArchiveParty", (), {"party_id": party_id})()
            result = ArchivePartyUseCase(party_repo).execute(cmd)
            self.wfile.write(json.dumps({"success": result.success, "data": result.data}).encode())

    def do_PUT(self):
        content_len = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(content_len)) if content_len else {}
        path = self.path.rstrip("/")

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()

        if path.startswith("/api/parties/"):
            party_id = path.split("/")[-1]
            cmd = CreateParty(party_id=party_id, payload=body)
            result = UpdatePartyUseCase(party_repo).execute(cmd)
            self.wfile.write(json.dumps({
                "success": result.success,
                "data": result.data,
                "errors": result.errors
            }).encode())

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()


if __name__ == "__main__":
    import urllib.parse

    # Seed demo data
    from business_core.domain.party.party import Party

    p1 = Party.create_person("João", "Silva", "João Silva")
    from business_core.domain.party.party_role import PartyRole, PartyRoleType, RoleStatus
    p1.add_role(PartyRole(PartyRoleType.CUSTOMER))
    p1.add_role(PartyRole(PartyRoleType.EMPLOYEE))
    from business_core.domain.party.document import Document, DocumentType
    from business_core.domain.party.party_document import PartyDocument
    p1.add_document(PartyDocument(DocumentType.CPF, "529.982.247-25", True))
    p1.clear_events()
    party_repo.save(p1)

    p2 = Party.create_organization("Empresa Exemplo Ltda", "Exemplo")
    from business_core.domain.party.address import Address
    from business_core.domain.party.party_address import PartyAddress, AddressType
    addr = Address(street="Av. Paulista", number="1000", city="São Paulo", region="SP", postal_code="01310-100")
    p2.add_address(PartyAddress(addr, AddressType.MAIN, True))
    p2.add_role(PartyRole(PartyRoleType.SUPPLIER))
    p2.add_role(PartyRole(PartyRoleType.CUSTOMER))
    p2.add_document(PartyDocument(DocumentType.CNPJ, "11.222.333/0001-81", True))
    p2.clear_events()
    party_repo.save(p2)

    print(f"🚀 BusinessCore Party API rodando em http://localhost:{PORT}")
    print(f"📋 Acesse: http://localhost:{PORT}/pages/party.html")
    server = http.server.HTTPServer(("0.0.0.0", PORT), PartyAPIHandler)
    server.serve_forever()
