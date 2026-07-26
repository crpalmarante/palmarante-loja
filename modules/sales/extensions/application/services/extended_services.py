from modules.sales.extensions.domain.entities.agreement import CustomerAgreement
from modules.sales.extensions.domain.entities.calendar import CalendarEvent, CalendarEventType
from modules.sales.extensions.domain.entities.audit import AuditEntry
from modules.sales.extensions.domain.entities.events import SalesEvent, SalesEventType


class AgreementService:
    def __init__(self, repo):
        self._repo = repo

    def create(self, customer_id: str, name: str = '', **kwargs) -> CustomerAgreement:
        ag = CustomerAgreement(customer_id=customer_id, name=name or name, **kwargs)
        return self._repo.save_agreement(ag)

    def find_by_customer(self, customer_id: str) -> list:
        return self._repo.find_agreements(customer_id)

    def find_active(self, customer_id: str) -> CustomerAgreement | None:
        agreements = self._repo.find_agreements(customer_id)
        for ag in agreements:
            if ag.is_valid():
                return ag
        return None

    def apply_to_order(self, customer_id: str, order_data: dict) -> dict:
        ag = self.find_active(customer_id)
        if ag:
            return ag.apply_to_order(order_data)
        return order_data


class CalendarService:
    def __init__(self, repo):
        self._repo = repo

    def add_event(self, title: str, date: str, **kwargs) -> CalendarEvent:
        ev = CalendarEvent(title=title, date=date, **kwargs)
        return self._repo.save_calendar_event(ev)

    def list_events(self, date_from: str = '', date_to: str = '',
                    sales_rep: str = '') -> list:
        events = self._repo.find_calendar_events(sales_rep)
        if date_from:
            events = [e for e in events if e.date >= date_from]
        if date_to:
            events = [e for e in events if e.date <= date_to]
        return events

    def generate_from_order(self, document_id: str, customer_id: str,
                            customer_name: str, expected_delivery: str,
                            sales_rep: str = '') -> CalendarEvent:
        return self.add_event(
            title=f'Entrega Pedido', date=expected_delivery,
            event_type=CalendarEventType.DELIVERY,
            customer_id=customer_id, customer_name=customer_name,
            document_id=document_id, sales_rep=sales_rep,
        )


class OrderSplitService:
    def __init__(self, repo):
        self._repo = repo

    def split_by_warehouse(self, document_id: str, warehouse_map: dict) -> list:
        results = []
        for wh_id, line_ids in warehouse_map.items():
            split = {
                'original_document_id': document_id,
                'warehouse_id': wh_id,
                'line_ids': line_ids,
                'status': 'pending',
            }
            results.append(split)
        return results

    def split_by_availability(self, document_id: str, lines: list) -> dict:
        available = []
        unavailable = []
        for line in lines:
            item_id = line.get('item_id', '')
            qty = line.get('quantity', 1)
            try:
                from modules.sales.core.application.services import clients
                avail = clients.get_availability(item_id)
                data = avail.get('data', avail)
                if data.get('available', 0) >= qty:
                    available.append(line)
                else:
                    unavailable.append(line)
            except Exception:
                available.append(line)
        return {'available': available, 'unavailable': unavailable,
                'original_document_id': document_id}


class DeliverySchedulingService:
    def __init__(self, repo):
        self._repo = repo

    def schedule(self, document_id: str, delivery_type: str = 'standard',
                 scheduled_date: str = '', address: str = '',
                 notes: str = '', created_by: str = '') -> dict:
        schedule = {
            'document_id': document_id,
            'delivery_type': delivery_type,
            'scheduled_date': scheduled_date or '',
            'address': address,
            'notes': notes,
            'status': 'scheduled',
            'created_by': created_by,
        }
        from datetime import datetime
        schedule['created_at'] = datetime.now().isoformat()
        return schedule

    def estimate(self, customer_zip: str = '') -> dict:
        return {
            'today': 'same_day',
            'tomorrow': 'next_day',
            'scheduled': 'scheduled',
            'estimated_days': 1 if customer_zip else 2,
        }


class CustomerPreferencesService:
    def __init__(self, repo):
        self._repo = repo

    def get(self, customer_id: str) -> dict:
        prefs = self._repo.find_customer_preferences(customer_id)
        if prefs:
            return prefs
        return {'customer_id': customer_id}

    def set(self, customer_id: str, **kwargs) -> dict:
        prefs = self._repo.find_customer_preferences(customer_id) or {}
        prefs.update(kwargs)
        prefs['customer_id'] = customer_id
        return self._repo.save_customer_preferences(prefs)


class KpiEngine:
    def __init__(self, repo):
        self._repo = repo

    def calculate(self, days: int = 30) -> dict:
        orders = self._repo.find_sales_orders()
        opps = self._repo.find_opportunities()
        now = __import__('datetime').datetime.now()

        period_orders = [o for o in orders if o.created_at and
                         (now - o.created_at).days <= days]
        completed = [o for o in period_orders if o.status.value == 'completed']
        total_revenue = sum(o.total for o in completed)
        total_orders = len(completed)
        total_lines = sum(len(o.lines) for o in completed)
        won_opps = [o for o in opps if o.status.value == 'won']
        total_opps = len([o for o in opps if o.status.value != 'lost'])

        return {
            'period_days': days,
            'total_orders': total_orders,
            'total_revenue': round(total_revenue, 2),
            'avg_ticket': round(total_revenue / total_orders, 2) if total_orders > 0 else 0,
            'avg_margin': 0.0,
            'orders_per_day': round(total_orders / days, 1) if days > 0 else 0,
            'products_sold': total_lines,
            'conversion_rate': round(len(won_opps) / total_opps * 100, 1) if total_opps > 0 else 0,
            'active_customers': len(set(o.customer_id for o in completed)),
            'new_customers': 0,
        }


class ValidationEngine:
    def __init__(self, repo):
        self._repo = repo
        self._clients = None

    @property
    def clients(self):
        if self._clients is None:
            from modules.sales.core.application.services import clients
            self._clients = clients
        return self._clients

    def validate_order(self, customer_id: str = '', items: list = None,
                       order_total: float = 0, discount_total: float = 0,
                       price_list_id: str = '', **kwargs) -> dict:
        if items is None:
            items = []
        errors = []
        warnings = []

        if customer_id:
            try:
                party = self.clients.get_party(customer_id)
                if not party:
                    errors.append('Cliente não encontrado')
            except Exception:
                errors.append('Erro ao consultar cliente')

        for item in items:
            item_id = item.get('item_id', '')
            qty = item.get('quantity', 0)
            price = item.get('unit_price', 0)
            if item_id:
                try:
                    it = self.clients.get_item(item_id)
                    if not it:
                        errors.append(f'Item {item_id} não encontrado')
                    elif not it.get('active', True):
                        errors.append(f'Item {item_id} inativo')
                except Exception:
                    pass
                if qty <= 0:
                    errors.append(f'Quantidade inválida para {item_id}')
                if price <= 0:
                    warnings.append(f'Item {item_id} sem preço')

        if order_total <= 0 and items:
            warnings.append('Valor total zerado')

        max_disc = order_total * 0.5
        if discount_total > max_disc:
            warnings.append(f'Desconto acima de 50% ({discount_total})')

        return {
            'valid': len(errors) == 0,
            'errors': errors,
            'warnings': warnings,
            'can_proceed': len(errors) == 0,
        }


class AuditService:
    def __init__(self, repo):
        self._repo = repo

    def record(self, entity_type: str, entity_id: str, field_name: str,
               old_value: str, new_value: str, changed_by: str = '',
               change_type: str = 'update', document_id: str = '') -> AuditEntry:
        entry = AuditEntry(
            entity_type=entity_type, entity_id=entity_id,
            field_name=field_name, old_value=str(old_value),
            new_value=str(new_value), changed_by=changed_by,
            change_type=change_type, document_id=document_id,
        )
        return self._repo.save_audit_entry(entry)

    def history(self, entity_type: str = '', entity_id: str = '',
                document_id: str = '', limit: int = 100) -> list:
        entries = self._repo.find_audit_entries(entity_type, entity_id, document_id)
        entries.sort(key=lambda e: e.created_at, reverse=True)
        return entries[:limit]


class EventService:
    def __init__(self, repo):
        self._repo = repo

    def emit(self, event_type: SalesEventType, **kwargs) -> SalesEvent:
        event = SalesEvent(event_type=event_type, **kwargs)
        event = self._repo.save_event(event)
        self._notify_hooks(event)
        return event

    def _notify_hooks(self, event: SalesEvent):
        pass

    def list_by_document(self, document_id: str) -> list:
        events = self._repo.find_events(document_id=document_id)
        events.sort(key=lambda e: e.created_at)
        return events

    def list_by_customer(self, customer_id: str) -> list:
        events = self._repo.find_events(customer_id=customer_id)
        events.sort(key=lambda e: e.created_at, reverse=True)
        return events


class HookManager:
    def __init__(self):
        self._hooks = {}

    def register(self, hook_point: str, handler):
        if hook_point not in self._hooks:
            self._hooks[hook_point] = []
        self._hooks[hook_point].append(handler)

    def execute(self, hook_point: str, context: dict = None) -> dict:
        if context is None:
            context = {}
        results = []
        for handler in self._hooks.get(hook_point, []):
            try:
                result = handler(context)
                results.append(result)
            except Exception as e:
                results.append({'error': str(e)})
        return {'hook_point': hook_point, 'results': results, 'context': context}

    def run_before(self, hook_point: str, context: dict = None) -> dict:
        return self.execute(f'before_{hook_point}', context)

    def run_after(self, hook_point: str, context: dict = None) -> dict:
        return self.execute(f'after_{hook_point}', context)


class SearchService:
    def __init__(self, repo):
        self._repo = repo

    def search(self, query: str, limit: int = 10) -> dict:
        q = query.lower()
        results = {'orders': [], 'customers': [], 'products': [],
                   'quotations': [], 'contracts': []}

        orders = self._repo.find_sales_orders()
        for o in orders:
            if q in o.customer_name.lower() or q in o.document_number.lower():
                results['orders'].append({
                    'id': o._id, 'type': 'order',
                    'title': f'{o.document_number} - {o.customer_name}',
                    'status': o.status.value,
                })
                if len(results['orders']) >= limit:
                    break

        opps = self._repo.find_opportunities()
        customers_seen = set()
        for o in opps:
            cid = o.customer_id
            if cid not in customers_seen and (q in o.customer_name.lower() or q in cid.lower()):
                results['customers'].append({
                    'id': cid, 'type': 'customer',
                    'title': o.customer_name or cid,
                })
                customers_seen.add(cid)
                if len(results['customers']) >= limit:
                    break

        for o in orders:
            for line in o.lines:
                if q in line.item_name.lower() or q in line.item_code.lower():
                    results['products'].append({
                        'id': line.item_id, 'type': 'product',
                        'title': f'{line.item_name} ({line.item_code})',
                    })
                    if len(results['products']) >= limit:
                        break

        contracts = self._repo.find_contracts()
        for c in contracts:
            if q in c.title.lower() or q in c.contract_number.lower():
                results['contracts'].append({
                    'id': c._id, 'type': 'contract',
                    'title': f'{c.contract_number} - {c.title}',
                })
                if len(results['contracts']) >= limit:
                    break

        return results


class SalesIntelligence:
    def __init__(self, repo):
        self._repo = repo

    def inactive_customers(self, days: int = 90) -> list:
        from datetime import datetime, timedelta
        cutoff = datetime.now() - timedelta(days=days)
        active = set()
        orders = self._repo.find_sales_orders()
        for o in orders:
            if o.created_at and o.created_at >= cutoff:
                active.add(o.customer_id)
        all_customers = set()
        for o in orders:
            all_customers.add(o.customer_id)
        inativos = [{'customer_id': c} for c in all_customers if c not in active]
        return inativos

    def top_products(self, limit: int = 10) -> list:
        sales_count = {}
        orders = self._repo.find_sales_orders()
        for o in orders:
            for line in o.lines:
                pid = line.item_id
                if pid not in sales_count:
                    sales_count[pid] = {'item_id': pid, 'item_name': line.item_name,
                                        'total_qty': 0, 'total_value': 0}
                sales_count[pid]['total_qty'] += line.quantity
                sales_count[pid]['total_value'] += line.total
        sorted_items = sorted(sales_count.values(),
                              key=lambda x: x['total_value'], reverse=True)
        return sorted_items[:limit]

    def sales_forecast(self, months: int = 3) -> dict:
        orders = self._repo.find_sales_orders()
        completed = [o for o in orders if o.status.value == 'completed']
        if not completed:
            return {'forecast': 0, 'avg_monthly': 0, 'months': months}
        from datetime import datetime
        total_revenue = sum(o.total for o in completed)
        dates = [o.created_at for o in completed if o.created_at]
        if not dates:
            return {'forecast': 0, 'avg_monthly': 0, 'months': months}
        first = min(dates)
        last = max(dates)
        days_span = max((last - first).days, 1)
        monthly_avg = total_revenue / max(days_span / 30, 1)
        return {
            'avg_monthly': round(monthly_avg, 2),
            'forecast': round(monthly_avg * months, 2),
            'months': months,
        }

    def executive_panel(self) -> dict:
        kpi = KpiEngine(self._repo).calculate(30)
        top = self.top_products(5)
        inactive = self.inactive_customers(90)
        forecast = self.sales_forecast(3)
        return {
            'kpi': kpi,
            'top_products': top,
            'inactive_customers': len(inactive),
            'forecast': forecast,
            'alerts': self._alerts(kpi),
        }

    def _alerts(self, kpi: dict) -> list:
        alerts = []
        if kpi.get('total_orders', 0) == 0:
            alerts.append({'type': 'warning', 'message': 'Nenhum pedido no período'})
        if kpi.get('conversion_rate', 100) < 20:
            alerts.append({'type': 'alert', 'message': 'Taxa de conversão abaixo de 20%'})
        return alerts
