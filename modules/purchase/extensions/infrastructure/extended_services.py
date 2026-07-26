from datetime import datetime


class PriceHistoryService:
    def __init__(self, repo):
        self._repo = repo
        self._history = []

    def record(self, item_id: str, supplier_id: str, unit_price: float,
               quantity: float = 0, po_number: str = '', notes: str = '') -> dict:
        entry = {
            '_id': f'ph_{datetime.now().timestamp()}',
            'item_id': item_id, 'supplier_id': supplier_id,
            'unit_price': unit_price, 'quantity': quantity,
            'po_number': po_number, 'notes': notes,
            'created_at': datetime.now().isoformat(),
        }
        self._history.append(entry)
        return entry

    def for_item(self, item_id: str) -> list:
        entries = [e for e in self._history if e['item_id'] == item_id]
        entries.sort(key=lambda e: e['created_at'], reverse=True)
        return entries

    def for_supplier_item(self, supplier_id: str, item_id: str) -> list:
        entries = [e for e in self._history
                   if e['supplier_id'] == supplier_id and e['item_id'] == item_id]
        entries.sort(key=lambda e: e['created_at'], reverse=True)
        return entries

    def best_price(self, item_id: str) -> dict | None:
        entries = self.for_item(item_id)
        if not entries: return None
        return min(entries, key=lambda e: e['unit_price'])


class LastPurchasesService:
    def __init__(self, repo):
        self._repo = repo

    def for_item(self, item_id: str, limit: int = 5) -> list:
        orders = self._repo.find_purchase_orders()
        results = []
        for po in orders:
            for line in po.lines:
                if line.item_id == item_id:
                    results.append({
                        'po_id': po._id, 'po_number': po.document_number,
                        'supplier_id': po.supplier_id,
                        'supplier_name': po.supplier_name,
                        'unit_price': line.unit_price,
                        'quantity': line.quantity,
                        'total': line.total,
                        'date': po.created_at.isoformat() if hasattr(po.created_at, 'isoformat') else str(po.created_at),
                    })
        results.sort(key=lambda r: r['date'], reverse=True)
        return results[:limit]


class SplitPurchaseService:
    def __init__(self, repo):
        self._repo = repo

    def split_order(self, po_id: str, splits: list) -> list:
        po = self._repo.find_purchase_order_by_id(po_id)
        if not po: return []
        results = []
        for split in splits:
            supplier_id = split['supplier_id']
            supplier_name = split.get('supplier_name', '')
            items = split.get('items', [])
            lines = []
            for si in items:
                orig = next((l for l in po.lines if l._id == si.get('line_id')), None)
                if orig:
                    qty = si.get('quantity', orig.quantity)
                    lines.append(type('', (), {
                        'item_id': orig.item_id, 'item_code': orig.item_code,
                        'item_name': orig.item_name, 'quantity': qty,
                        'unit_price': orig.unit_price, 'total': orig.unit_price * qty,
                    })())
            if lines:
                new_po = self._repo.save_purchase_order(
                    type('PurchaseOrder', (), {
                        'document_id': '', 'document_number': '',
                        'supplier_id': supplier_id, 'supplier_name': supplier_name,
                        'lines': lines, 'total': sum(l.total for l in lines),
                        'status': type('Status', (), {'value': 'draft'})(),
                        'created_at': datetime.now(), '_id': '',
                    })()
                )
                results.append({'po_id': new_po._id, 'supplier_name': supplier_name,
                                'total': sum(l.total for l in lines)})
        return results


class ScheduledDeliveryService:
    def schedule(self, po_id: str, deliveries: list) -> list:
        schedules = []
        for d in deliveries:
            schedules.append({
                'po_id': po_id,
                'date': d.get('date', ''),
                'quantity': d.get('quantity', 0),
                'item_id': d.get('item_id', ''),
                'status': 'scheduled',
                'created_at': datetime.now().isoformat(),
            })
        return schedules


class PurchasePolicyEngine:
    def __init__(self, repo):
        self._repo = repo
        self._policies = []

    def add_policy(self, name: str, condition_field: str, condition_operator: str,
                   condition_value: str, action: str, action_value: str = '',
                   scope: str = 'global', priority: int = 0) -> dict:
        policy = {
            '_id': f'pp_{datetime.now().timestamp()}',
            'name': name, 'condition_field': condition_field,
            'condition_operator': condition_operator,
            'condition_value': condition_value,
            'action': action, 'action_value': action_value,
            'scope': scope, 'priority': priority, 'active': True,
        }
        self._policies.append(policy)
        return policy

    def evaluate(self, context: dict) -> list:
        results = []
        for p in self._policies:
            if not p['active']:
                continue
            val = str(context.get(p['condition_field'], ''))
            target = p['condition_value']
            match = False
            if p['condition_operator'] == 'equals':
                match = val == target
            elif p['condition_operator'] == 'greater_than':
                try: match = float(val) > float(target)
                except: pass
            elif p['condition_operator'] == 'less_than':
                try: match = float(val) < float(target)
                except: pass
            elif p['condition_operator'] == 'in':
                match = val in target.split(',')
            if match:
                results.append(p)
        return results


class ValidationEngine:
    def validate_po(self, po_data: dict) -> dict:
        errors = []
        warns = []
        if not po_data.get('supplier_id'):
            errors.append('Fornecedor não informado')
        items = po_data.get('lines', [])
        if not items:
            errors.append('Nenhum item no pedido')
        for item in items:
            qty = item.get('quantity', 0)
            price = item.get('unit_price', 0)
            if qty <= 0:
                errors.append(f'Quantidade inválida para {item.get("item_id", "")}')
            if price <= 0:
                warns.append(f'Preço zero para {item.get("item_id", "")}')
        total = po_data.get('total', 0)
        if total > 100000:
            warns.append('Pedido acima de R$ 100.000 - aprovação especial')
        return {'valid': len(errors) == 0, 'errors': errors, 'warnings': warns}


class PurchaseEventService:
    def __init__(self):
        self._events = []

    def emit(self, event_type: str, **kw) -> dict:
        event = {'_id': f'pev_{datetime.now().timestamp()}',
                 'event_type': event_type, 'data': kw,
                 'created_at': datetime.now().isoformat()}
        self._events.append(event)
        return event

    def list_by_document(self, document_id: str) -> list:
        return [e for e in self._events
                if e['data'].get('document_id') == document_id]


class PurchaseTimeline:
    def __init__(self, repo):
        self._repo = repo
        self._entries = []

    def add(self, document_id: str, title: str, description: str = '',
            created_by: str = '', entry_type: str = 'general') -> dict:
        entry = {
            '_id': f'ptl_{datetime.now().timestamp()}',
            'document_id': document_id, 'title': title,
            'description': description, 'created_by': created_by,
            'entry_type': entry_type,
            'created_at': datetime.now().isoformat(),
        }
        self._entries.append(entry)
        return entry

    def for_document(self, document_id: str) -> list:
        return [e for e in self._entries if e['document_id'] == document_id]


class PurchaseDashboard:
    def __init__(self, repo):
        self._repo = repo

    def build(self) -> dict:
        orders = self._repo.find_purchase_orders()
        total_orders = len(orders)
        total_value = sum(o.total for o in orders)
        pending = [o for o in orders if o.status.value in ('draft', 'pending_approval')]
        approved = [o for o in orders if o.status.value == 'approved']
        receipts = self._repo.find_goods_receipts()
        completed_receipts = [r for r in receipts if r.status.value == 'completed']
        suppliers = set(o.supplier_name for o in orders)

        top = {}
        for o in orders:
            name = o.supplier_name or o.supplier_id
            top[name] = top.get(name, 0) + o.total
        top_suppliers = sorted(top.items(), key=lambda x: -x[1])[:5]

        return {
            'total_orders': total_orders,
            'total_value': round(total_value, 2),
            'pending_approval': len(pending),
            'approved': len(approved),
            'receipts': len(completed_receipts),
            'suppliers': len(suppliers),
            'avg_order_value': round(total_value / total_orders, 2) if total_orders else 0,
            'top_suppliers': [{'name': k, 'total': round(v, 2)} for k, v in top_suppliers],
        }


class StrategicSourcing:
    def __init__(self, repo):
        self._repo = repo
        self._supplier_catalog = {}
        self._risk_assessments = {}
        self._preferred_suppliers = {}
        self._multi_supplier = {}

    def homologate(self, supplier_id: str, documents: list = None,
                   approved: bool = False, notes: str = '') -> dict:
        entry = {
            'supplier_id': supplier_id,
            'documents': documents or [],
            'approved': approved,
            'notes': notes,
            'status': 'approved' if approved else 'pending',
            'homologated_at': datetime.now().isoformat(),
        }
        self._supplier_catalog[supplier_id] = entry
        return entry

    def assess_risk(self, supplier_id: str, financial_score: float = 0,
                    delivery_risk: str = 'medium', overall_risk: str = 'medium',
                    notes: str = '') -> dict:
        assessment = {
            'supplier_id': supplier_id,
            'financial_score': financial_score,
            'delivery_risk': delivery_risk,
            'overall_risk': overall_risk,
            'notes': notes,
            'assessed_at': datetime.now().isoformat(),
        }
        self._risk_assessments[supplier_id] = assessment
        return assessment

    def set_preferred(self, supplier_id: str, item_id: str = '',
                      priority: int = 1) -> dict:
        entry = {'supplier_id': supplier_id, 'item_id': item_id, 'priority': priority}
        key = f'{supplier_id}:{item_id}'
        self._preferred_suppliers[key] = entry
        return entry

    def add_multi_supplier(self, item_id: str, suppliers: list) -> dict:
        self._multi_supplier[item_id] = suppliers
        return {'item_id': item_id, 'suppliers': suppliers}

    def get_suppliers_for_item(self, item_id: str) -> list:
        results = []
        for key, val in self._preferred_suppliers.items():
            if val.get('item_id') == item_id:
                results.append(val)
        results.sort(key=lambda x: x.get('priority', 99))
        return results

    def supplier_summary(self, supplier_id: str) -> dict:
        scores = self._repo.find_vendor_scores(supplier_id)
        avg_score = 0
        if scores:
            avg_score = sum(s.criteria.overall_score for s in scores) / len(scores)
        return {
            'supplier_id': supplier_id,
            'homologated': supplier_id in self._supplier_catalog,
            'risk': self._risk_assessments.get(supplier_id, {}),
            'avg_score': round(avg_score, 1),
            'total_evaluations': len(scores),
        }
