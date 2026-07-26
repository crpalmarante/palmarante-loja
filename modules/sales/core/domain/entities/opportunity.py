from dataclasses import dataclass, field
from datetime import datetime
from modules.sales.core.domain.value_objects.sales_status import OpportunityStatus


@dataclass
class Opportunity:
    title: str
    customer_id: str
    customer_name: str = ''
    pipeline_id: str = ''
    stage: str = 'new'
    status: OpportunityStatus = OpportunityStatus.NEW
    expected_value: float = 0.0
    probability: int = 10
    notes: str = ''
    source: str = ''
    sales_rep: str = ''
    expected_close: str = ''
    items: list = None
    won_at: datetime = None
    lost_reason: str = ''
    created_at: datetime = None
    updated_at: datetime = None
    _id: str = ''

    def __post_init__(self):
        if self.items is None:
            self.items = []
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = datetime.now()

    def win(self):
        self.status = OpportunityStatus.WON
        self.won_at = datetime.now()
        self.updated_at = datetime.now()

    def lose(self, reason: str = ''):
        self.status = OpportunityStatus.LOST
        self.lost_reason = reason
        self.updated_at = datetime.now()


@dataclass
class Pipeline:
    name: str
    stages: list = None
    active: bool = True
    created_at: datetime = None
    _id: str = ''

    def __post_init__(self):
        if self.stages is None:
            self.stages = ['new', 'qualified', 'proposal', 'negotiation', 'won', 'lost']
        if self.created_at is None:
            self.created_at = datetime.now()


@dataclass
class PipelineStage:
    name: str
    sort_order: int = 0
    probability: int = 50
    color: str = '#1a73e8'
