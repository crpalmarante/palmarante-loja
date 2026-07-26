from modules.sales.core.domain.entities.opportunity import Opportunity, Pipeline
from modules.sales.core.domain.entities.price_list import PriceList, PriceListItem
from modules.sales.core.domain.entities.discount_rule import DiscountRule
from modules.sales.core.domain.entities.commission import CommissionRule, CommissionStatement
from modules.sales.core.domain.entities.contract import Contract
from modules.sales.core.domain.entities.delivery import Delivery
from modules.sales.core.domain.entities.return_request import ReturnRequest
from modules.sales.core.domain.entities.sales_order import SalesOrder
from modules.sales.core.domain.repositories.sales_repository import SalesRepository


class SalesRepositoryMemory(SalesRepository):
    _counter = 0
    _template_counter = 0
    _favorite_counter = 0
    _price_history_counter = 0
    _timeline_counter = 0
    _note_counter = 0
    _tag_counter = 0
    _team_counter = 0
    _approval_counter = 0
    _credit_counter = 0
    _bundle_counter = 0
    _campaign_counter = 0
    _policy_counter = 0
    _rule_counter = 0
    _agreement_counter = 0
    _calendar_counter = 0
    _pref_counter = 0
    _audit_counter = 0
    _event_counter = 0

    def __init__(self):
        self._sales_orders = {}
        self._opportunities = {}
        self._pipelines = {}
        self._price_lists = {}
        self._discount_rules = {}
        self._commission_rules = {}
        self._statements = {}
        self._contracts = {}
        self._deliveries = {}
        self._returns = {}
        self._templates = {}
        self._favorites = {}
        self._price_history = {}
        self._timeline = {}
        self._notes = {}
        self._tags = {}
        self._team_members = {}
        self._approval_rules = {}
        self._credits = {}
        self._bundles = {}
        self._campaigns = {}
        self._policies = {}
        self._rules = {}
        self._agreements = {}
        self._calendar_events = {}
        self._preferences = {}
        self._audit_entries = {}
        self._events = {}

    def _next_id(self) -> str:
        self.__class__._counter += 1
        return str(self.__class__._counter)

    # ── Sales Orders ────────────────────────────────────────────
    def save_sales_order(self, so: SalesOrder) -> SalesOrder:
        if not so._id:
            so._id = self._next_id()
        self._sales_orders[so._id] = so
        return so

    def find_sales_order_by_id(self, so_id: str) -> SalesOrder | None:
        return self._sales_orders.get(so_id)

    def find_sales_order_by_document(self, document_id: str) -> SalesOrder | None:
        for so in self._sales_orders.values():
            if so.document_id == document_id:
                return so
        return None

    def find_sales_orders(self, customer_id: str = '', status: str = '',
                          document_type: str = '', limit: int = 100) -> list:
        results = list(self._sales_orders.values())
        if customer_id:
            results = [so for so in results if so.customer_id == customer_id]
        if status:
            results = [so for so in results if so.status.value == status]
        if document_type:
            results = [so for so in results if so.document_type == document_type]
        results.sort(key=lambda so: so.created_at, reverse=True)
        return results[:limit]

    # ── Opportunities ───────────────────────────────────────────
    def save_opportunity(self, opp: Opportunity) -> Opportunity:
        if not opp._id:
            opp._id = self._next_id()
        self._opportunities[opp._id] = opp
        return opp

    def find_opportunity_by_id(self, opp_id: str) -> Opportunity | None:
        return self._opportunities.get(opp_id)

    def find_opportunities(self, customer_id: str = '', status: str = '',
                           sales_rep: str = '', limit: int = 100) -> list:
        results = list(self._opportunities.values())
        if customer_id:
            results = [o for o in results if o.customer_id == customer_id]
        if status:
            results = [o for o in results if o.status.value == status]
        if sales_rep:
            results = [o for o in results if o.sales_rep == sales_rep]
        results.sort(key=lambda o: o.created_at, reverse=True)
        return results[:limit]

    # ── Pipelines ───────────────────────────────────────────────
    def save_pipeline(self, p: Pipeline) -> Pipeline:
        if not p._id:
            p._id = self._next_id()
        self._pipelines[p._id] = p
        return p

    def find_pipeline_by_id(self, pid: str) -> Pipeline | None:
        return self._pipelines.get(pid)

    def find_all_pipelines(self) -> list[Pipeline]:
        return list(self._pipelines.values())

    # ── Price Lists ─────────────────────────────────────────────
    def save_price_list(self, pl: PriceList) -> PriceList:
        if not pl._id:
            pl._id = self._next_id()
        self._price_lists[pl._id] = pl
        return pl

    def find_price_list_by_id(self, pl_id: str) -> PriceList | None:
        return self._price_lists.get(pl_id)

    def find_price_list_by_code(self, code: str) -> PriceList | None:
        for pl in self._price_lists.values():
            if pl.code == code:
                return pl
        return None

    def find_all_price_lists(self) -> list[PriceList]:
        return list(self._price_lists.values())

    # ── Discount Rules ──────────────────────────────────────────
    def save_discount_rule(self, r: DiscountRule) -> DiscountRule:
        if not r._id:
            r._id = self._next_id()
        self._discount_rules[r._id] = r
        return r

    def find_discount_rule_by_id(self, rid: str) -> DiscountRule | None:
        return self._discount_rules.get(rid)

    def find_active_discount_rules(self) -> list[DiscountRule]:
        return [r for r in self._discount_rules.values() if r.active]

    # ── Commissions ─────────────────────────────────────────────
    def save_commission_rule(self, r: CommissionRule) -> CommissionRule:
        if not r._id:
            r._id = self._next_id()
        self._commission_rules[r._id] = r
        return r

    def find_commission_rules(self, sales_rep_id: str = '') -> list:
        results = list(self._commission_rules.values())
        if sales_rep_id:
            results = [r for r in results if not r.sales_rep_ids or sales_rep_id in r.sales_rep_ids]
        return results

    def save_statement(self, s: CommissionStatement) -> CommissionStatement:
        if not s._id:
            s._id = self._next_id()
        self._statements[s._id] = s
        return s

    # ── Contracts ───────────────────────────────────────────────
    def save_contract(self, c: Contract) -> Contract:
        if not c._id:
            c._id = self._next_id()
        self._contracts[c._id] = c
        return c

    def find_contract_by_id(self, cid: str) -> Contract | None:
        return self._contracts.get(cid)

    def find_contracts(self, customer_id: str = '', status: str = '') -> list:
        results = list(self._contracts.values())
        if customer_id:
            results = [c for c in results if c.customer_id == customer_id]
        if status:
            results = [c for c in results if c.status.value == status]
        return results

    # ── Deliveries ──────────────────────────────────────────────
    def save_delivery(self, d: Delivery) -> Delivery:
        if not d._id:
            d._id = self._next_id()
        self._deliveries[d._id] = d
        return d

    def find_delivery_by_id(self, did: str) -> Delivery | None:
        return self._deliveries.get(did)

    def find_deliveries(self, document_id: str = '', status: str = '') -> list:
        results = list(self._deliveries.values())
        if document_id:
            results = [d for d in results if d.document_id == document_id]
        if status:
            results = [d for d in results if d.status.value == status]
        return results

    # ── Returns ─────────────────────────────────────────────────
    def save_return(self, r: ReturnRequest) -> ReturnRequest:
        if not r._id:
            r._id = self._next_id()
        self._returns[r._id] = r
        return r

    def find_returns(self, document_id: str = '', status: str = '') -> list:
        results = list(self._returns.values())
        if document_id:
            results = [r for r in results if r.document_id == document_id]
        if status:
            results = [r for r in results if r.status.value == status]
        return results

    # ── Sales Experience ────────────────────────────────────────
    def save_template(self, t) -> any:
        self._template_counter += 1
        if not t._id:
            t._id = f'tpl_{self._template_counter}'
        self._templates[t._id] = t
        return t

    def find_template_by_id(self, tid: str):
        return self._templates.get(tid)

    def find_templates(self, customer_id: str = '') -> list:
        results = list(self._templates.values())
        if customer_id:
            results = [t for t in results if t.customer_id == customer_id]
        return results

    def save_favorite(self, f) -> any:
        self._favorite_counter += 1
        if not f._id:
            f._id = f'fav_{self._favorite_counter}'
        self._favorites[f._id] = f
        return f

    def find_favorites(self, customer_id: str) -> list:
        return [f for f in self._favorites.values() if f.customer_id == customer_id]

    def remove_favorite(self, favorite_id: str):
        self._favorites.pop(favorite_id, None)

    def save_price_history(self, entry) -> any:
        self._price_history_counter += 1
        if not entry._id:
            entry._id = f'ph_{self._price_history_counter}'
        self._price_history[entry._id] = entry
        return entry

    def find_price_history(self, item_id: str, limit: int = 20) -> list:
        results = [e for e in self._price_history.values() if e.item_id == item_id]
        results.sort(key=lambda e: e.created_at, reverse=True)
        return results[:limit]

    def save_timeline_entry(self, entry) -> any:
        self._timeline_counter += 1
        if not entry._id:
            entry._id = f'tl_{self._timeline_counter}'
        self._timeline[entry._id] = entry
        return entry

    def find_timeline(self, document_id: str) -> list:
        results = [e for e in self._timeline.values() if e.document_id == document_id]
        results.sort(key=lambda e: e.created_at)
        return results

    def save_note(self, note) -> any:
        self._note_counter += 1
        if not note._id:
            note._id = f'note_{self._note_counter}'
        self._notes[note._id] = note
        return note

    def find_notes(self, document_id: str, note_type: str = '') -> list:
        results = [n for n in self._notes.values() if n.document_id == document_id]
        if note_type:
            results = [n for n in results if n.note_type.value == note_type]
        return results

    def save_tag(self, tag) -> any:
        self._tag_counter += 1
        if not tag._id:
            tag._id = f'tag_{self._tag_counter}'
        self._tags[tag._id] = tag
        return tag

    def find_tag_by_id(self, tag_id: str):
        return self._tags.get(tag_id)

    def find_tags(self) -> list:
        return list(self._tags.values())

    def save_team_member(self, member) -> any:
        self._team_counter += 1
        if not member._id:
            member._id = f'team_{self._team_counter}'
        self._team_members[member._id] = member
        return member

    def find_team_members(self, role: str = '') -> list:
        results = list(self._team_members.values())
        if role:
            results = [m for m in results if m.role == role]
        return results

    def find_team_member_by_id(self, rep_id: str):
        for m in self._team_members.values():
            if m.rep_id == rep_id:
                return m
        return None

    def save_approval_rule(self, rule) -> any:
        self._approval_counter += 1
        if not rule._id:
            rule._id = f'app_{self._approval_counter}'
        self._approval_rules[rule._id] = rule
        return rule

    def find_approval_rules(self) -> list:
        return list(self._approval_rules.values())

    def find_approver_for_value(self, order_value: float) -> str:
        rules = sorted(self._approval_rules.values(), key=lambda r: r.min_value, reverse=True)
        for rule in rules:
            if rule.active and rule.matches(order_value):
                return rule.approver_role
        return 'seller'

    # ── Extensions ─────────────────────────────────────────
    # Credit
    def save_credit(self, c):
        self._credit_counter += 1
        if not c._id:
            c._id = f'cred_{self._credit_counter}'
        self._credits[c._id] = c
        return c

    def find_credit_by_customer(self, customer_id: str):
        for c in self._credits.values():
            if c.customer_id == customer_id:
                return c
        return None

    # Bundles
    def save_bundle(self, b):
        self._bundle_counter += 1
        if not b._id:
            b._id = f'bndl_{self._bundle_counter}'
        self._bundles[b._id] = b
        return b

    def find_bundles(self) -> list:
        return list(self._bundles.values())

    def find_bundle_by_id(self, bid: str):
        return self._bundles.get(bid)

    # Campaigns
    def save_campaign(self, c):
        self._campaign_counter += 1
        if not c._id:
            c._id = f'camp_{self._campaign_counter}'
        self._campaigns[c._id] = c
        return c

    def find_campaigns(self) -> list:
        return list(self._campaigns.values())

    # Policies
    def save_policy(self, p):
        self._policy_counter += 1
        if not p._id:
            p._id = f'pol_{self._policy_counter}'
        self._policies[p._id] = p
        return p

    def find_policies(self) -> list:
        return list(self._policies.values())

    # Rules
    def save_rule(self, r):
        self._rule_counter += 1
        if not r._id:
            r._id = f'rule_{self._rule_counter}'
        self._rules[r._id] = r
        return r

    def find_rules(self) -> list:
        return list(self._rules.values())

    # Recommendations
    def find_similar_items(self, item_id: str, limit: int = 3) -> list:
        return []

    def find_cross_sell_items(self, item_id: str, limit: int = 3) -> list:
        return []

    def find_up_sell_items(self, item_id: str, limit: int = 3) -> list:
        return []

    # Agreements
    def save_agreement(self, a):
        self._agreement_counter += 1
        if not a._id:
            a._id = f'agr_{self._agreement_counter}'
        self._agreements[a._id] = a
        return a

    def find_agreements(self, customer_id: str = '') -> list:
        results = list(self._agreements.values())
        if customer_id:
            results = [a for a in results if a.customer_id == customer_id]
        return results

    # Calendar
    def save_calendar_event(self, e):
        self._calendar_counter += 1
        if not e._id:
            e._id = f'cal_{self._calendar_counter}'
        self._calendar_events[e._id] = e
        return e

    def find_calendar_events(self, sales_rep: str = '') -> list:
        results = list(self._calendar_events.values())
        if sales_rep:
            results = [e for e in results if e.sales_rep == sales_rep]
        return results

    # Customer Preferences
    def save_customer_preferences(self, p: dict) -> dict:
        self._pref_counter += 1
        pid = p.get('_id') or f'pref_{self._pref_counter}'
        p['_id'] = pid
        self._preferences[pid] = p
        return p

    def find_customer_preferences(self, customer_id: str) -> dict | None:
        for p in self._preferences.values():
            if p.get('customer_id') == customer_id:
                return p
        return None

    # Audit
    def save_audit_entry(self, e):
        self._audit_counter += 1
        if not e._id:
            e._id = f'aud_{self._audit_counter}'
        self._audit_entries[e._id] = e
        return e

    def find_audit_entries(self, entity_type: str = '', entity_id: str = '',
                           document_id: str = '') -> list:
        results = list(self._audit_entries.values())
        if entity_type:
            results = [e for e in results if e.entity_type == entity_type]
        if entity_id:
            results = [e for e in results if e.entity_id == entity_id]
        if document_id:
            results = [e for e in results if e.document_id == document_id]
        return results

    # Events
    def save_event(self, e):
        self._event_counter += 1
        if not e._id:
            e._id = f'evt_{self._event_counter}'
        self._events[e._id] = e
        return e

    def find_events(self, document_id: str = '', customer_id: str = '') -> list:
        results = list(self._events.values())
        if document_id:
            results = [e for e in results if e.document_id == document_id]
        if customer_id:
            results = [e for e in results if e.customer_id == customer_id]
        return results
