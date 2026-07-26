import uvicorn
from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from modules.item.domain.entities.item import ItemType, ItemUnit
from modules.item.domain.value_objects.item_id import ItemId
from modules.item.infrastructure.postgres.memory_repository import InMemoryItemRepository
from modules.item.application.commands.item_commands import (
    CreateItem, UpdateItem, ActivateItem, DeactivateItem, ArchiveItem,
    ChangePrice, AddBarcode, AddVariant,
)
from modules.item.application.use_cases.create_item import CreateItemUseCase
from modules.item.application.use_cases.update_item import UpdateItemUseCase
from modules.item.application.use_cases.activate_item import ActivateItemUseCase
from modules.item.application.use_cases.change_price import ChangePriceUseCase
from modules.item.application.use_cases.add_barcode import AddBarcodeUseCase
from modules.item.application.use_cases.add_variant import AddVariantUseCase

app = FastAPI(title='BusinessCore — Item Module', version='2.0.0')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

repo = InMemoryItemRepository()
create_uc = CreateItemUseCase(repo)
update_uc = UpdateItemUseCase(repo)
activate_uc = ActivateItemUseCase(repo)
change_price_uc = ChangePriceUseCase(repo)
add_barcode_uc = AddBarcodeUseCase(repo)
add_variant_uc = AddVariantUseCase(repo)


def item_to_dict(i):
    return {
        'id': str(i.id),
        'name': i.name,
        'item_type': i.item_type.value,
        'sku': str(i.sku) if i.sku else '',
        'ncm': str(i.ncm) if i.ncm else '',
        'cest': str(i.cest) if i.cest else '',
        'ean': str(i.ean) if i.ean else '',
        'gtin': str(i.gtin) if i.gtin else '',
        'unit': i.unit.value,
        'cost_price': i.cost_price,
        'sale_price': i.sale_price,
        'brand': i.brand,
        'supplier_id': i.supplier_id or '',
        'notes': i.notes,
        'status': i.status.value,
        'stock': i.stock,
        'min_stock': i.min_stock,
        'barcodes': [{'code': b.code, 'type': b.barcode_type.value, 'is_main': b.is_main} for b in i.barcodes],
        'variants': [{'name': v.name, 'sku': v.sku, 'sale_price': v.sale_price} for v in i.variants],
        'created_at': i.created_at.isoformat(),
        'updated_at': i.updated_at.isoformat(),
    }


@app.get('/api/items')
def list_items(
    query: str = Query(''),
    status: str = Query(''),
    item_type: str = Query(''),
    offset: int = Query(0),
    limit: int = Query(50),
):
    items = repo.find_all(query, status, item_type, offset=offset, limit=limit)
    total = repo.count(query, status, item_type)
    return {'data': [item_to_dict(i) for i in items], 'total': total, 'offset': offset, 'limit': limit}


@app.get('/api/items/{item_id}')
def get_item(item_id: str):
    item = repo.find_by_id(ItemId.from_string(item_id))
    if not item:
        raise HTTPException(404, 'Item not found')
    return {'data': item_to_dict(item)}


@app.post('/api/items')
def create_item(body: dict):
    cmd = CreateItem(
        name=body.get('name', ''),
        item_type=ItemType(body.get('item_type', 'product')),
        sku=body.get('sku', ''),
        ncm=body.get('ncm', ''),
        cest=body.get('cest', ''),
        ean=body.get('ean', ''),
        gtin=body.get('gtin', ''),
        unit=ItemUnit(body.get('unit', 'unit')),
        cost_price=body.get('cost_price', 0.0),
        sale_price=body.get('sale_price', 0.0),
        category_id=body.get('category_id'),
        supplier_id=body.get('supplier_id', ''),
        brand=body.get('brand', ''),
        notes=body.get('notes', ''),
        stock=body.get('stock', 0.0),
        min_stock=body.get('min_stock', 0.0),
    )
    item = create_uc.execute(cmd)
    return {'data': item_to_dict(item)}


@app.put('/api/items/{item_id}')
def update_item(item_id: str, body: dict):
    cmd = UpdateItem(
        item_id=ItemId.from_string(item_id),
        name=body.get('name'),
        sku=body.get('sku'),
        ncm=body.get('ncm'),
        cest=body.get('cest'),
        ean=body.get('ean'),
        gtin=body.get('gtin'),
        unit=ItemUnit(body['unit']) if 'unit' in body else None,
        cost_price=body.get('cost_price'),
        sale_price=body.get('sale_price'),
        category_id=body.get('category_id'),
        supplier_id=body.get('supplier_id'),
        brand=body.get('brand'),
        notes=body.get('notes'),
        min_stock=body.get('min_stock'),
    )
    item = update_uc.execute(cmd)
    return {'data': item_to_dict(item)}


@app.post('/api/items/{item_id}/price')
def change_price(item_id: str, body: dict):
    change_price_uc.execute(ChangePrice(
        item_id=ItemId.from_string(item_id),
        cost_price=body.get('cost_price'),
        sale_price=body.get('sale_price'),
        reason=body.get('reason', ''),
    ))
    return {'status': 'ok'}


@app.post('/api/items/{item_id}/barcodes')
def add_barcode(item_id: str, body: dict):
    from modules.item.domain.entities.barcode import BarcodeType
    add_barcode_uc.execute(AddBarcode(
        item_id=ItemId.from_string(item_id),
        code=body.get('code', ''),
        barcode_type=BarcodeType(body.get('type', 'ean13')),
        is_main=body.get('is_main', False),
    ))
    return {'status': 'ok'}


@app.post('/api/items/{item_id}/variants')
def add_variant(item_id: str, body: dict):
    add_variant_uc.execute(AddVariant(
        item_id=ItemId.from_string(item_id),
        name=body.get('name', ''),
        sku=body.get('sku', ''),
        sale_price=body.get('sale_price', 0.0),
        cost_price=body.get('cost_price', 0.0),
        stock=body.get('stock', 0.0),
    ))
    return {'status': 'ok'}


@app.post('/api/items/{item_id}/activate')
def activate_item(item_id: str):
    activate_uc.activate(ActivateItem(item_id=ItemId.from_string(item_id)))
    return {'status': 'ok'}


@app.post('/api/items/{item_id}/deactivate')
def deactivate_item(item_id: str):
    activate_uc.deactivate(DeactivateItem(item_id=ItemId.from_string(item_id)))
    return {'status': 'ok'}


@app.post('/api/items/{item_id}/archive')
def archive_item(item_id: str):
    activate_uc.archive(ArchiveItem(item_id=ItemId.from_string(item_id)))
    return {'status': 'ok'}


@app.delete('/api/items/{item_id}')
def delete_item(item_id: str):
    repo.delete(ItemId.from_string(item_id))
    return {'status': 'ok'}


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8001)
