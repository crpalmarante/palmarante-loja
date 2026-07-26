from modules.inventory.domain.repositories.inventory_repository import InventoryRepository


class AvailabilityEngine:
    def __init__(self, repo: InventoryRepository):
        self._repo = repo

    def get_balance(self, item_id: str, warehouse_id: str = '',
                    location_id: str = '', lot_id: str = '') -> dict:
        physical = self._repo.compute_balance(item_id, warehouse_id, location_id, lot_id)
        reserved = sum(
            r.quantity for r in self._repo.find_reservations(item_id, warehouse_id, 'active')
            if (not location_id or r.location_id == location_id)
            and (not lot_id or r.lot_id == lot_id)
        )
        return {
            'item_id': item_id,
            'warehouse_id': warehouse_id or '*',
            'physical': physical,
            'reserved': reserved,
            'available': physical - reserved,
        }

    def is_available(self, item_id: str, warehouse_id: str, quantity: float) -> bool:
        balance = self.get_balance(item_id, warehouse_id)
        return balance['available'] >= quantity

    def get_balances(self, item_id: str = '', warehouse_id: str = '') -> list[dict]:
        movements = self._repo.find_movements(item_id=item_id, warehouse_id=warehouse_id)
        items = set()
        whs = set()
        for m in movements:
            items.add(m.item_id)
            whs.add(m.warehouse_id)
        results = []
        for iid in items:
            for wid in whs:
                results.append(self.get_balance(iid, wid))
        if not results:
            if item_id:
                results.append(self.get_balance(item_id, warehouse_id or ''))
        return results

    def get_dashboard(self) -> dict:
        all_movements = self._repo.find_movements()
        total_items = len(set(m.item_id for m in all_movements))
        total_in = sum(m.quantity for m in all_movements if m.is_entry and m.status.value == 'confirmed')
        total_out = sum(m.quantity for m in all_movements if m.is_exit and m.status.value == 'confirmed')
        active_reservations = self._repo.find_reservations(status='active')
        total_reserved = sum(r.quantity for r in active_reservations)
        pending_transfers = self._repo.find_transfers(status='draft') + self._repo.find_transfers(status='sent')
        today = [m for m in all_movements if m.created_at and m.created_at.date() == __import__('datetime').date.today()]
        return {
            'total_items_in_stock': total_items,
            'total_value': 0,
            'total_reserved': total_reserved,
            'total_available': total_in - total_out - total_reserved,
            'movements_today': len(today),
            'inventory_counts_pending': len(self._repo.find_counts_by_warehouse('')),
            'transfers_pending': len(pending_transfers),
            'expired_lots': len(self._repo.find_expired_lots()),
        }
