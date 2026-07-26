import uvicorn
from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from decimal import Decimal

from modules.catalog.infrastructure.postgres.memory_repository import InMemoryCatalogRepository
from modules.catalog.domain.entities.attribute import AttributeType
from modules.catalog.domain.entities.unit import UnitType

app = FastAPI(title='BusinessCore — Catalog Module', version='1.0.0')
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_credentials=True, allow_methods=['*'], allow_headers=['*'])

repo = InMemoryCatalogRepository()


# ---- Categories ----
@app.get('/api/catalog/categories')
def list_categories(query: str = Query(''), active: bool | None = None):
    cats = repo.find_all_categories(query, active)
    return {'data': [{'id': c._id, 'name': c.name, 'parent_id': c.parent_id, 'code': c.code, 'active': c.active} for c in cats]}


@app.post('/api/catalog/categories')
def create_category(body: dict):
    from modules.catalog.domain.entities.category import Category
    cat = Category(name=body['name'], parent_id=body.get('parent_id'), code=body.get('code', ''), description=body.get('description', ''))
    repo.save_category(cat)
    return {'data': {'id': cat._id, 'name': cat.name}}


# ---- Brands ----
@app.get('/api/catalog/brands')
def list_brands(query: str = Query(''), active: bool | None = None):
    brands = repo.find_all_brands(query, active)
    return {'data': [{'id': b._id, 'name': b.name, 'code': b.code, 'active': b.active} for b in brands]}


@app.post('/api/catalog/brands')
def create_brand(body: dict):
    from modules.catalog.domain.entities.brand import Brand
    b = Brand(name=body['name'], code=body.get('code', ''))
    repo.save_brand(b)
    return {'data': {'id': b._id, 'name': b.name}}


# ---- Manufacturers ----
@app.get('/api/catalog/manufacturers')
def list_manufacturers(query: str = Query('')):
    mfs = repo.find_all_manufacturers(query)
    return {'data': [{'id': m._id, 'name': m.name, 'cnpj': m.cnpj} for m in mfs]}


@app.post('/api/catalog/manufacturers')
def create_manufacturer(body: dict):
    from modules.catalog.domain.entities.manufacturer import Manufacturer
    m = Manufacturer(name=body['name'], cnpj=body.get('cnpj', ''))
    repo.save_manufacturer(m)
    return {'data': {'id': m._id, 'name': m.name}}


# ---- Units ----
@app.get('/api/catalog/units')
def list_units(active: bool | None = None):
    units = repo.find_all_units(active)
    return {'data': [{'code': u.code, 'name': u.name, 'type': u.type.value} for u in units]}


@app.post('/api/catalog/units')
def create_unit(body: dict):
    from modules.catalog.domain.entities.unit import Unit
    u = Unit(code=body['code'], name=body['name'], type=UnitType(body.get('type', 'units')))
    repo.save_unit(u)
    return {'data': {'code': u.code, 'name': u.name}}


# ---- Conversions ----
@app.post('/api/catalog/conversions')
def create_conversion(body: dict):
    from modules.catalog.domain.entities.unit_conversion import UnitConversion
    c = UnitConversion(from_code=body['from_code'], to_code=body['to_code'], factor=Decimal(str(body['factor'])))
    repo.save_conversion(c)
    return {'data': {'from': c.from_code, 'to': c.to_code, 'factor': str(c.factor)}}


# ---- Attributes ----
@app.get('/api/catalog/attributes')
def list_attributes(active: bool | None = None):
    attrs = repo.find_all_attributes(active)
    return {'data': [{'id': a._id, 'name': a.name, 'code': a.code, 'type': a.type.value} for a in attrs]}


@app.post('/api/catalog/attributes')
def create_attribute(body: dict):
    from modules.catalog.domain.entities.attribute import Attribute
    a = Attribute(name=body['name'], code=body.get('code', ''), type=AttributeType(body.get('type', 'text')), required=body.get('required', False))
    repo.save_attribute(a)
    return {'data': {'id': a._id, 'name': a.name}}


# ---- Attribute Values ----
@app.get('/api/catalog/attributes/{attr_id}/values')
def list_attribute_values(attr_id: str):
    vals = repo.find_values_by_attribute(attr_id)
    return {'data': [{'id': v._id, 'value': v.value, 'code': v.code, 'sort_order': v.sort_order} for v in vals]}


@app.post('/api/catalog/attributes/{attr_id}/values')
def create_attribute_value(attr_id: str, body: dict):
    from modules.catalog.domain.entities.attribute_value import AttributeValue
    v = AttributeValue(attribute_id=attr_id, value=body['value'], code=body.get('code', ''), sort_order=body.get('sort_order', 0))
    repo.save_attribute_value(v)
    return {'data': {'id': v._id, 'value': v.value}}


# ---- Variants ----
@app.get('/api/catalog/variants')
def list_variants(item_id: str = Query('')):
    if item_id:
        variants = repo.find_variants_by_item(item_id)
    else:
        variants = []
    return {'data': [{'item_id': v.item_id, 'sku': v.sku, 'name': v.display_name, 'attributes': v.attribute_values} for v in variants]}


@app.post('/api/catalog/variants')
def create_variant(body: dict):
    from modules.catalog.domain.entities.variant import Variant
    v = Variant(item_id=body['item_id'], sku=body.get('sku', ''), name=body.get('name', ''), attribute_values=body.get('attribute_values', {}))
    repo.save_variant(v)
    return {'data': {'item_id': v.item_id, 'sku': v.sku, 'name': v.display_name}}


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8003)
