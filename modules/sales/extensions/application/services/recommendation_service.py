from modules.sales.extensions.domain.entities.bundle import SalesBundle, BundleItem


class RecommendationService:
    def __init__(self, repo):
        self._repo = repo

    def find_similar(self, item_id: str, limit: int = 3) -> list:
        items = self._repo.find_similar_items(item_id)
        return items[:limit]

    def find_cross_sell(self, item_id: str, limit: int = 3) -> list:
        suggestions = self._repo.find_cross_sell_items(item_id)
        return suggestions[:limit]

    def find_up_sell(self, item_id: str, limit: int = 3) -> list:
        suggestions = self._repo.find_up_sell_items(item_id)
        return suggestions[:limit]

    def find_bundles(self, item_id: str = '') -> list:
        all_bundles = self._repo.find_bundles()
        if item_id:
            return [b for b in all_bundles
                    if any(bi.item_id == item_id for bi in (b.items or []))]
        return all_bundles

    def get_bundle_items(self, bundle_id: str) -> list:
        bundle = self._repo.find_bundle_by_id(bundle_id)
        if not bundle:
            return []
        return bundle.items
