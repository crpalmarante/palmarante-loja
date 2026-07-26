from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class VendorScoreCriteria:
    price_score: float = 0.0
    delivery_score: float = 0.0
    quality_score: float = 0.0
    service_score: float = 0.0
    overall_score: float = 0.0

    def calculate(self):
        self.overall_score = (
            self.price_score * 0.3 +
            self.delivery_score * 0.25 +
            self.quality_score * 0.25 +
            self.service_score * 0.2
        )


@dataclass
class VendorScoreEntry:
    supplier_id: str
    supplier_name: str = ''
    po_id: str = ''
    po_number: str = ''
    criteria: VendorScoreCriteria = None
    on_time_delivery: bool = True
    defect_rate: float = 0.0
    price_competitiveness: float = 0.0
    communication_rating: float = 0.0
    notes: str = ''
    evaluated_by: str = ''
    created_at: datetime = None
    _id: str = ''

    def __post_init__(self):
        if self.criteria is None:
            self.criteria = VendorScoreCriteria()
        if self.created_at is None:
            self.created_at = datetime.now()

    def calculate_score(self):
        price = max(0, min(100, self.price_competitiveness))
        delivery = 100 if self.on_time_delivery else 30
        quality = max(0, 100 - self.defect_rate * 10)
        service = max(0, min(100, self.communication_rating))
        self.criteria = VendorScoreCriteria(
            price_score=price,
            delivery_score=delivery,
            quality_score=quality,
            service_score=service,
        )
        self.criteria.calculate()
        return self.criteria.overall_score
