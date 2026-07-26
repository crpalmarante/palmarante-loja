import uvicorn
from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from modules.inventory.infrastructure.postgres.memory_repository import InMemoryInventoryRepository
from modules.inventory.application.use_cases.record_movement import RecordMovementUseCase
from modules.inventory.application.use_cases.manage_lot import CreateLotUseCase
from modules.inventory.application.commands.inventory_commands import (
    RecordMovement, CreateLot, RegisterSerial, CreateReservation, CancelReservation,
    CreateTransfer, CompleteTransfer, CreateInventoryCount, CompleteInventoryCount, CreateLocation,
)
from modules.inventory.application.services.availability_engine import AvailabilityEngine
from modules.inventory.domain.entities.serial_number import SerialNumber
from modules.inventory.domain.entities.location import Location
from modules.inventory.domain.entities.reservation import Reservation
from modules.inventory.domain.entities.transfer_order import TransferOrder

app = FastAPI(title='BusinessCore — Inventory Platform', version='2.0.0')
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_credentials=True, allow_methods=['*'], allow_headers=['*'])

repo = InMemoryInventoryRepository()
engine = AvailabilityEngine(repo)


# ── Dashboard ────────────────────────────────────────────────
@app.get('/api/inventory/dashboard')
def dashboard():
    return {'data': engine.get_dashboard()}


# ── Stock Ledger / Movements ─────────────────────────────────
@app.get('/api/inventory/movements')
def list_movements(item_id: str = Query(''), warehouse_id: str = Query(''),
                   movement_type: str = Query(''), reference_type: str = Query(''),
                   limit: int = Query(100)):
    movs = repo.find_movements(item_id, warehouse_id, movement_type, reference_type, limit)
    return {'data': [{'id': m._id, 'item_id': m.item_id, 'warehouse_id': m.warehouse_id,
                      'type': m.movement_type.value, 'quantity': m.quantity,
                      'location_id': m.location_id, 'lot_id': m.lot_id,
                      'reference_type': m.reference_type, 'reference_id': m.reference_id,
                      'document_number': m.document_number, 'status': m.status.value,
                      'created_at': m.created_at.isoformat() if m.created_at else ''} for m in movs]}


@app.post('/api/inventory/movements')
def create_movement(body: dict):
    uc = RecordMovementUseCase(repo)
    cmd = RecordMovement(
        item_id=body['item_id'], warehouse_id=body['warehouse_id'],
        movement_type=body['movement_type'], quantity=body['quantity'],
        location_id=body.get('location_id', ''), lot_id=body.get('lot_id', ''),
        serial_number=body.get('serial_number', ''),
        reference_type=body.get('reference_type', ''),
        reference_id=body.get('reference_id', ''),
        document_number=body.get('document_number', ''),
        unit_cost=body.get('unit_cost', 0), notes=body.get('notes', ''),
        created_by=body.get('created_by', ''))
    mov = uc.execute(cmd)
    return {'data': {'id': mov._id, 'type': mov.movement_type.value, 'quantity': mov.quantity, 'status': mov.status.value}}


# ── Balance (computed from ledger) ───────────────────────────
@app.get('/api/inventory/balance')
def balance(item_id: str = Query(''), warehouse_id: str = Query(''),
            location_id: str = Query(''), lot_id: str = Query('')):
    if not item_id:
        balances = engine.get_balances(item_id, warehouse_id)
        return {'data': balances}
    result = engine.get_balance(item_id, warehouse_id, location_id, lot_id)
    return {'data': [result]}


@app.get('/api/inventory/available')
def available(item_id: str, warehouse_id: str = '', quantity: float = Query(0)):
    if quantity > 0:
        return {'data': {'available': engine.is_available(item_id, warehouse_id or '', quantity)}}
    bal = engine.get_balance(item_id, warehouse_id or '')
    return {'data': {'physical': bal['physical'], 'reserved': bal['reserved'], 'available': bal['available']}}


# ── Locations ────────────────────────────────────────────────
@app.get('/api/inventory/locations')
def list_locations(warehouse_id: str = Query('')):
    if not warehouse_id:
        return {'data': []}
    locs = repo.find_locations_by_warehouse(warehouse_id)
    return {'data': [{'id': l._id, 'code': l.code, 'name': l.name, 'type': l.type, 'level': l.level} for l in locs]}


@app.post('/api/inventory/locations')
def create_location(body: dict):
    loc = Location(warehouse_id=body['warehouse_id'], code=body['code'],
                   name=body.get('name', ''), parent_id=body.get('parent_id', ''),
                   type=body.get('type', 'rack'))
    repo.save_location(loc)
    return {'data': {'id': loc._id, 'code': loc.code}}


# ── Lots ─────────────────────────────────────────────────────
@app.get('/api/inventory/lots')
def list_lots(item_id: str = Query(''), warehouse_id: str = Query(''), expiring_days: int = Query(0)):
    if expiring_days > 0:
        lots = repo.find_expiring_lots(expiring_days)
    else:
        lots = repo.find_lots_by_item(item_id, warehouse_id) if item_id else [l for l in repo._lots.values() if l.status.value == 'active']
    return {'data': [{'id': l._id, 'item_id': l.item_id, 'warehouse_id': l.warehouse_id,
                      'lot_number': l.lot_number, 'supplier_lot': l.supplier_lot,
                      'manufacturing_date': str(l.manufacturing_date) if l.manufacturing_date else '',
                      'expiry_date': str(l.expiry_date) if l.expiry_date else '',
                      'status': l.status.value, 'origin': l.origin} for l in lots]}


@app.post('/api/inventory/lots')
def create_lot(body: dict):
    uc = CreateLotUseCase(repo)
    cmd = CreateLot(item_id=body['item_id'], warehouse_id=body['warehouse_id'],
                    lot_number=body['lot_number'], supplier_lot=body.get('supplier_lot', ''),
                    manufacturing_date=body.get('manufacturing_date', ''),
                    expiry_date=body.get('expiry_date', ''),
                    origin=body.get('origin', ''), notes=body.get('notes', ''))
    lot = uc.execute(cmd)
    return {'data': {'id': lot._id, 'lot_number': lot.lot_number}}


@app.get('/api/inventory/lots/expired')
def expired_lots():
    lots = repo.find_expired_lots()
    return {'data': [{'id': l._id, 'item_id': l.item_id, 'lot_number': l.lot_number,
                      'quantity': 0, 'expiry_date': str(l.expiry_date)} for l in lots]}


# ── Serials ──────────────────────────────────────────────────
@app.get('/api/inventory/serials')
def list_serials(item_id: str = Query(''), warehouse_id: str = Query(''), status: str = Query('')):
    serials = repo.find_serials(item_id, warehouse_id, status)
    return {'data': [{'id': s._id, 'serial': s.serial, 'item_id': s.item_id,
                      'warehouse_id': s.warehouse_id, 'status': s.status.value,
                      'lot_id': s.lot_id, 'location_id': s.location_id} for s in serials]}


@app.post('/api/inventory/serials')
def register_serial(body: dict):
    existing = repo.find_serial(body['serial'])
    if existing:
        raise HTTPException(409, f'Serial {body["serial"]} already exists')
    s = SerialNumber(item_id=body['item_id'], warehouse_id=body['warehouse_id'],
                     serial=body['serial'], lot_id=body.get('lot_id', ''),
                     location_id=body.get('location_id', ''), notes=body.get('notes', ''))
    repo.save_serial(s)
    return {'data': {'id': s._id, 'serial': s.serial, 'status': s.status.value}}


@app.post('/api/inventory/serials/{serial}/reserve')
def reserve_serial(serial: str):
    s = repo.find_serial(serial)
    if not s:
        raise HTTPException(404, 'Serial not found')
    s.reserve()
    repo.save_serial(s)
    return {'data': {'serial': s.serial, 'status': s.status.value}}


@app.post('/api/inventory/serials/{serial}/sell')
def sell_serial(serial: str):
    s = repo.find_serial(serial)
    if not s:
        raise HTTPException(404, 'Serial not found')
    s.sell()
    repo.save_serial(s)
    return {'data': {'serial': s.serial, 'status': s.status.value}}


# ── Reservations ─────────────────────────────────────────────
@app.get('/api/inventory/reservations')
def list_reservations(item_id: str = Query(''), warehouse_id: str = Query(''),
                      status: str = Query('active'), order_id: str = Query('')):
    reservations = repo.find_reservations(item_id, warehouse_id, status, order_id=order_id)
    return {'data': [{'id': r._id, 'item_id': r.item_id, 'warehouse_id': r.warehouse_id,
                      'quantity': r.quantity, 'status': r.status.value,
                      'order_type': r.order_type, 'order_id': r.order_id,
                      'created_at': r.created_at.isoformat() if r.created_at else ''} for r in reservations]}


@app.post('/api/inventory/reservations')
def create_reservation(body: dict):
    r = repo.save_reservation(Reservation(
        item_id=body['item_id'], warehouse_id=body['warehouse_id'],
        quantity=body['quantity'], order_type=body.get('order_type', ''),
        order_id=body.get('order_id', ''), location_id=body.get('location_id', ''),
        lot_id=body.get('lot_id', ''), notes=body.get('notes', ''),
        created_by=body.get('created_by', '')))
    return {'data': {'id': r._id, 'status': r.status.value}}


@app.post('/api/inventory/reservations/{rid}/cancel')
def cancel_reservation(rid: str):
    reservations = repo.find_reservations(order_id=rid)
    if not reservations:
        raise HTTPException(404, 'Reservation not found')
    r = reservations[0]
    r.cancel()
    repo.save_reservation(r)
    return {'data': {'id': r._id, 'status': r.status.value}}


# ── Transfers ────────────────────────────────────────────────
@app.get('/api/inventory/transfers')
def list_transfers(warehouse_id: str = Query(''), status: str = Query('')):
    transfers = repo.find_transfers(warehouse_id, status)
    return {'data': [{'id': t._id, 'from': t.from_warehouse_id, 'to': t.to_warehouse_id,
                      'status': t.status.value, 'items': len(t.items),
                      'created_at': t.created_at.isoformat() if t.created_at else ''} for t in transfers]}


@app.post('/api/inventory/transfers')
def create_transfer(body: dict):
    t = repo.save_transfer(TransferOrder(
        from_warehouse_id=body['from_warehouse_id'],
        to_warehouse_id=body['to_warehouse_id'],
        items=body.get('items', []), notes=body.get('notes', ''),
        created_by=body.get('created_by', '')))
    return {'data': {'id': t._id, 'status': t.status.value}}


@app.post('/api/inventory/transfers/{tid}/send')
def send_transfer(tid: str):
    t = repo.find_transfer_by_id(tid)
    if not t:
        raise HTTPException(404, 'Transfer not found')
    t.send()
    repo.save_transfer(t)
    return {'data': {'id': t._id, 'status': t.status.value}}


@app.post('/api/inventory/transfers/{tid}/receive')
def receive_transfer(tid: str):
    t = repo.find_transfer_by_id(tid)
    if not t:
        raise HTTPException(404, 'Transfer not found')
    t.receive()
    repo.save_transfer(t)
    return {'data': {'id': t._id, 'status': t.status.value}}


@app.post('/api/inventory/transfers/{tid}/complete')
def complete_transfer(tid: str):
    t = repo.find_transfer_by_id(tid)
    if not t:
        raise HTTPException(404, 'Transfer not found')
    t.complete()
    repo.save_transfer(t)
    return {'data': {'id': t._id, 'status': t.status.value}}


# ── Inventory Counts ─────────────────────────────────────────
@app.get('/api/inventory/counts')
def list_counts(warehouse_id: str = Query('')):
    counts = repo.find_counts_by_warehouse(warehouse_id)
    return {'data': [{'id': c._id, 'warehouse_id': c.warehouse_id,
                      'status': c.status.value, 'lines': c.line_count,
                      'total_difference': c.total_difference,
                      'counted_by': c.counted_by,
                      'created_at': c.created_at.isoformat() if c.created_at else ''} for c in counts]}


@app.post('/api/inventory/counts')
def create_count(body: dict):
    from modules.inventory.domain.entities.inventory_count import InventoryCount, CountLine
    lines = [CountLine(**l) for l in body.get('lines', [])]
    c = InventoryCount(warehouse_id=body['warehouse_id'], lines=lines,
                       counted_by=body.get('counted_by', ''), notes=body.get('notes', ''))
    repo.save_count(c)
    return {'data': {'id': c._id, 'lines': c.line_count}}


@app.post('/api/inventory/counts/{cid}/complete')
def complete_count(cid: str):
    counts = [c for c in repo._counts if c._id == cid]
    if not counts:
        raise HTTPException(404, 'Count not found')
    c = counts[0]
    c.complete()
    repo.save_count(c)
    return {'data': {'id': c._id, 'total_difference': c.total_difference}}


# ── Traceability ─────────────────────────────────────────────
@app.get('/api/inventory/trace')
def trace(item_id: str = Query(''), serial: str = Query(''), lot_number: str = Query('')):
    if serial:
        s = repo.find_serial(serial)
        if not s:
            raise HTTPException(404, 'Serial not found')
        movs = repo.find_movements(item_id=s.item_id, warehouse_id=s.warehouse_id)
        return {'data': {'serial': s.serial, 'item_id': s.item_id, 'warehouse_id': s.warehouse_id,
                         'status': s.status.value, 'lot_id': s.lot_id,
                         'movements': len(movs)}}
    if lot_number:
        lots = [l for l in repo._lots.values() if l.lot_number == lot_number]
        if not lots:
            raise HTTPException(404, 'Lot not found')
        l = lots[0]
        movs = repo.find_movements(item_id=l.item_id, lot_id=l._id)
        return {'data': {'lot_number': l.lot_number, 'item_id': l.item_id,
                         'warehouse_id': l.warehouse_id, 'status': l.status.value,
                         'movements': len(movs)}}
    if item_id:
        movs = repo.find_movements(item_id=item_id)
        return {'data': {'item_id': item_id, 'movements': len(movs)}}
    raise HTTPException(400, 'Provide item_id, serial, or lot_number')


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8005)
