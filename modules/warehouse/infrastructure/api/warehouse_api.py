import uvicorn
from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from modules.warehouse.infrastructure.postgres.memory_repository import InMemoryWarehouseRepository
from modules.warehouse.application.use_cases.create_warehouse import CreateWarehouseUseCase
from modules.warehouse.application.use_cases.adjust_stock import AdjustStockUseCase
from modules.warehouse.application.use_cases.record_movement import RecordMovementUseCase
from modules.warehouse.application.commands.warehouse_commands import CreateWarehouse, AdjustStock, RecordMovement
from modules.warehouse.domain.entities.stock_movement import MovementType

app = FastAPI(title='BusinessCore — Warehouse Module', version='1.0.0')
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_credentials=True, allow_methods=['*'], allow_headers=['*'])

repo = InMemoryWarehouseRepository()


@app.get('/api/warehouses')
def list_warehouses(query: str = Query(''), active: bool | None = None):
    whs = repo.find_all_warehouses(query, active)
    return {'data': [{'id': w._id, 'name': w.name, 'code': w.code, 'active': w.active} for w in whs]}


@app.post('/api/warehouses')
def create_warehouse(body: dict):
    uc = CreateWarehouseUseCase(repo)
    cmd = CreateWarehouse(name=body['name'], code=body.get('code', ''),
                          description=body.get('description', ''),
                          address=body.get('address', ''),
                          responsible=body.get('responsible', ''))
    wh = uc.execute(cmd)
    return {'data': {'id': wh._id, 'name': wh.name, 'code': wh.code}}


@app.get('/api/warehouses/{wh_id}')
def get_warehouse(wh_id: str):
    wh = repo.find_warehouse_by_id(wh_id)
    if not wh:
        raise HTTPException(404, 'Warehouse not found')
    return {'data': {'id': wh._id, 'name': wh.name, 'code': wh.code, 'description': wh.description,
                     'address': wh.address, 'responsible': wh.responsible, 'active': wh.active}}


@app.get('/api/warehouses/{wh_id}/stock')
def list_stock(wh_id: str):
    stock = repo.find_stock_by_warehouse(wh_id)
    return {'data': [{'id': s._id, 'item_id': s.item_id, 'quantity': s.quantity,
                      'reserved': s.reserved, 'available': s.available,
                      'min_stock': s.min_stock, 'max_stock': s.max_stock} for s in stock]}


@app.post('/api/warehouses/{wh_id}/stock/adjust')
def adjust_stock(wh_id: str, body: dict):
    uc = AdjustStockUseCase(repo)
    cmd = AdjustStock(warehouse_id=wh_id, item_id=body['item_id'],
                      quantity=body['quantity'], notes=body.get('notes', ''))
    stock = uc.execute(cmd)
    return {'data': {'item_id': stock.item_id, 'quantity': stock.quantity}}


@app.get('/api/warehouses/{wh_id}/movements')
def list_movements(wh_id: str):
    movs = repo.find_movements_by_warehouse(wh_id)
    return {'data': [{'id': m._id, 'item_id': m.item_id, 'type': m.movement_type.value,
                      'quantity': m.quantity, 'status': m.status.value,
                      'created_at': m.created_at.isoformat() if m.created_at else ''} for m in movs]}


@app.post('/api/warehouses/{wh_id}/movements')
def create_movement(wh_id: str, body: dict):
    uc = RecordMovementUseCase(repo)
    cmd = RecordMovement(
        item_id=body['item_id'],
        warehouse_id=wh_id,
        movement_type=MovementType(body['movement_type']),
        quantity=body['quantity'],
        reference_type=body.get('reference_type', ''),
        reference_id=body.get('reference_id', ''),
        notes=body.get('notes', ''),
        target_warehouse_id=body.get('target_warehouse_id', ''),
    )
    mov = uc.execute(cmd)
    return {'data': {'id': mov._id, 'item_id': mov.item_id, 'type': mov.movement_type.value, 'quantity': mov.quantity}}


@app.get('/api/stock/low')
def low_stock():
    items = repo.find_low_stock()
    return {'data': [{'item_id': s.item_id, 'warehouse_id': s.warehouse_id,
                      'quantity': s.quantity, 'min_stock': s.min_stock} for s in items]}


@app.get('/api/stock')
def all_stock(item_id: str = Query(''), warehouse_id: str = Query('')):
    if item_id:
        items = repo.find_stock_by_item(item_id)
    elif warehouse_id:
        items = repo.find_stock_by_warehouse(warehouse_id)
    else:
        items = []
    return {'data': [{'id': s._id, 'item_id': s.item_id, 'warehouse_id': s.warehouse_id,
                      'quantity': s.quantity, 'available': s.available,
                      'min_stock': s.min_stock} for s in items]}


@app.get('/api/warehouses/{wh_id}/counts')
def list_counts(wh_id: str):
    counts = repo.find_counts_by_warehouse(wh_id)
    return {'data': [{'id': c._id, 'item_id': c.item_id,
                      'expected': c.expected_quantity, 'actual': c.actual_quantity,
                      'difference': c.difference, 'counted_by': c.counted_by} for c in counts]}


@app.post('/api/warehouses/{wh_id}/counts')
def create_count(wh_id: str, body: dict):
    from modules.warehouse.domain.entities.inventory_count import InventoryCount
    count = InventoryCount(warehouse_id=wh_id, item_id=body['item_id'],
                           expected_quantity=body.get('expected_quantity', 0),
                           actual_quantity=body['actual_quantity'],
                           counted_by=body.get('counted_by', ''),
                           notes=body.get('notes', ''))
    repo.save_inventory_count(count)
    return {'data': {'id': count._id, 'difference': count.difference}}


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8004)
