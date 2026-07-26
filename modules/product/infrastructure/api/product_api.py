import os
import uvicorn
from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from modules.product.domain.entities.product import ProductType, ProductUnit
from modules.product.infrastructure.postgres.memory_repository import InMemoryProductRepository
from modules.product.application.commands.product_commands import (
    CreateProduct, UpdateProduct, ActivateProduct, DeactivateProduct, ArchiveProduct,
)
from modules.product.application.use_cases.create_product import CreateProductUseCase
from modules.product.application.use_cases.update_product import UpdateProductUseCase
from modules.product.application.use_cases.activate_product import ActivateProductUseCase

app = FastAPI(title='BusinessCore — Product Module', version='1.0.0')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

repo = InMemoryProductRepository()

create_uc = CreateProductUseCase(repo)
update_uc = UpdateProductUseCase(repo)
activate_uc = ActivateProductUseCase(repo)


def product_to_dict(p):
    return {
        'id': str(p.id),
        'name': p.name,
        'product_type': p.product_type.value,
        'sku': str(p.sku) if p.sku else '',
        'ncm': str(p.ncm) if p.ncm else '',
        'ean': str(p.ean) if p.ean else '',
        'unit': p.unit.value,
        'cost_price': p.cost_price,
        'sale_price': p.sale_price,
        'category': p.category.name if p.category else '',
        'supplier_id': p.supplier_id or '',
        'notes': p.notes,
        'status': p.status.value,
        'stock': p.stock,
        'min_stock': p.min_stock,
        'created_at': p.created_at.isoformat(),
        'updated_at': p.updated_at.isoformat(),
    }


@app.get('/api/products')
def list_products(
    query: str = Query(''),
    status: str = Query(''),
    product_type: str = Query(''),
    category: str = Query(''),
    offset: int = Query(0),
    limit: int = Query(50),
):
    products = repo.find_all(query, status, product_type, category, offset, limit)
    total = repo.count(query, status, product_type, category)
    return {
        'data': [product_to_dict(p) for p in products],
        'total': total,
        'offset': offset,
        'limit': limit,
    }


@app.get('/api/products/{product_id}')
def get_product(product_id: str):
    from modules.product.domain.value_objects.product_id import ProductId
    pid = ProductId.from_string(product_id)
    product = repo.find_by_id(pid)
    if not product:
        raise HTTPException(404, 'Product not found')
    return {'data': product_to_dict(product)}


@app.post('/api/products')
def create_product(body: dict):
    cmd = CreateProduct(
        name=body.get('name', ''),
        product_type=ProductType(body.get('product_type', 'product')),
        sku=body.get('sku', ''),
        ncm=body.get('ncm', ''),
        ean=body.get('ean', ''),
        unit=ProductUnit(body.get('unit', 'unit')),
        cost_price=body.get('cost_price', 0.0),
        sale_price=body.get('sale_price', 0.0),
        category_name=body.get('category', ''),
        supplier_id=body.get('supplier_id', ''),
        notes=body.get('notes', ''),
        stock=body.get('stock', 0.0),
        min_stock=body.get('min_stock', 0.0),
    )
    product = create_uc.execute(cmd)
    return {'data': product_to_dict(product)}


@app.put('/api/products/{product_id}')
def update_product(product_id: str, body: dict):
    from modules.product.domain.value_objects.product_id import ProductId
    cmd = UpdateProduct(
        product_id=ProductId.from_string(product_id),
        name=body.get('name'),
        sku=body.get('sku'),
        ncm=body.get('ncm'),
        ean=body.get('ean'),
        unit=ProductUnit(body['unit']) if 'unit' in body else None,
        cost_price=body.get('cost_price'),
        sale_price=body.get('sale_price'),
        category_name=body.get('category'),
        supplier_id=body.get('supplier_id'),
        notes=body.get('notes'),
        min_stock=body.get('min_stock'),
    )
    product = update_uc.execute(cmd)
    return {'data': product_to_dict(product)}


@app.post('/api/products/{product_id}/activate')
def activate_product(product_id: str):
    from modules.product.domain.value_objects.product_id import ProductId
    activate_uc.activate(ActivateProduct(product_id=ProductId.from_string(product_id)))
    return {'status': 'ok'}


@app.post('/api/products/{product_id}/deactivate')
def deactivate_product(product_id: str):
    from modules.product.domain.value_objects.product_id import ProductId
    activate_uc.deactivate(DeactivateProduct(product_id=ProductId.from_string(product_id)))
    return {'status': 'ok'}


@app.post('/api/products/{product_id}/archive')
def archive_product(product_id: str):
    from modules.product.domain.value_objects.product_id import ProductId
    activate_uc.archive(ArchiveProduct(product_id=ProductId.from_string(product_id)))
    return {'status': 'ok'}


@app.delete('/api/products/{product_id}')
def delete_product(product_id: str):
    from modules.product.domain.value_objects.product_id import ProductId
    repo.delete(ProductId.from_string(product_id))
    return {'status': 'ok'}


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8001)
