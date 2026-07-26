"""HTTP client to emit notifications from any module to the Notification API."""
import urllib.request
import json

NOTIF_API_URL = 'http://localhost:8010/api/notifications'


def send_notification(user_id: str, title: str, message: str = '',
                      priority: str = 'normal', entity_type: str = '',
                      entity_id: str = '', icon: str = '',
                      action_url: str = '', category: str = '') -> dict | None:
    try:
        body = json.dumps({
            'user_id': user_id, 'title': title, 'message': message,
            'priority': priority, 'entity_type': entity_type,
            'entity_id': entity_id, 'icon': icon,
            'action_url': action_url, 'category': category,
        }).encode()
        req = urllib.request.Request(
            NOTIF_API_URL, data=body,
            headers={'Content-Type': 'application/json'},
            method='POST',
        )
        with urllib.request.urlopen(req, timeout=3) as resp:
            return json.loads(resp.read().decode())
    except Exception:
        return None


def notify_order_created(order_number: str, customer_name: str,
                         sales_rep: str = 'user-001', order_id: str = '') -> None:
    send_notification(
        user_id=sales_rep,
        title=f'Pedido {order_number} criado',
        message=f'Pedido de {customer_name} foi criado com sucesso.',
        entity_type='order', entity_id=order_id, icon='📋',
    )


def notify_order_approved(order_number: str, customer_name: str,
                          order_id: str = '', sales_rep: str = 'user-001') -> None:
    send_notification(
        user_id=sales_rep,
        title=f'Pedido {order_number} aprovado',
        message=f'O pedido de {customer_name} foi aprovado.',
        priority='high', entity_type='order', entity_id=order_id, icon='✅',
    )


def notify_order_cancelled(order_number: str, customer_name: str,
                           order_id: str = '', sales_rep: str = 'user-001') -> None:
    send_notification(
        user_id=sales_rep,
        title=f'Pedido {order_number} cancelado',
        message=f'O pedido de {customer_name} foi cancelado.',
        priority='high', entity_type='order', entity_id=order_id, icon='❌',
    )


def notify_order_shipped(order_number: str, customer_name: str,
                         order_id: str = '', sales_rep: str = 'user-001') -> None:
    send_notification(
        user_id=sales_rep,
        title=f'Pedido {order_number} enviado',
        message=f'O pedido de {customer_name} foi enviado ao cliente.',
        entity_type='order', entity_id=order_id, icon='🚚',
    )


def notify_quotation_created(quote_number: str, customer_name: str,
                             sales_rep: str = 'user-001', quote_id: str = '') -> None:
    send_notification(
        user_id=sales_rep,
        title=f'Orçamento {quote_number} criado',
        message=f'Orçamento para {customer_name} foi gerado.',
        entity_type='quotation', entity_id=quote_id, icon='💰',
    )


def notify_contract_created(contract_number: str, customer_name: str,
                            sales_rep: str = 'user-001', contract_id: str = '') -> None:
    send_notification(
        user_id=sales_rep,
        title=f'Contrato {contract_number} criado',
        message=f'Contrato com {customer_name} foi registrado.',
        entity_type='contract', entity_id=contract_id, icon='📑',
    )


def notify_purchase_request_created(request_number: str, requestor: str,
                                    approver: str = 'user-002',
                                    request_id: str = '') -> None:
    send_notification(
        user_id=approver,
        title=f'Requisição {request_number} aguarda aprovação',
        message=f'{requestor} solicitou {request_number}.',
        priority='high', entity_type='request', entity_id=request_id, icon='📋',
    )


def notify_purchase_order_created(po_number: str, supplier_name: str,
                                  buyer: str = 'user-001',
                                  po_id: str = '') -> None:
    send_notification(
        user_id=buyer,
        title=f'Pedido de compra {po_number} emitido',
        message=f'PO para {supplier_name} foi criada.',
        entity_type='purchase_order', entity_id=po_id, icon='📋',
    )


def notify_purchase_order_approved(po_number: str, supplier_name: str,
                                   buyer: str = 'user-001', po_id: str = '') -> None:
    send_notification(
        user_id=buyer,
        title=f'Pedido de compra {po_number} aprovado',
        message=f'A PO de {supplier_name} foi aprovada.',
        priority='high', entity_type='purchase_order', entity_id=po_id, icon='✅',
    )


def notify_goods_received(po_number: str, supplier_name: str,
                          receiver: str = 'user-001', po_id: str = '') -> None:
    send_notification(
        user_id=receiver,
        title=f'Recebimento parcial de {po_number}',
        message=f'Mercadorias de {supplier_name} recebidas.',
        entity_type='purchase_order', entity_id=po_id, icon='📦',
    )


def notify_rfq_opened(rfq_number: str, buyer: str = 'user-001',
                      rfq_id: str = '') -> None:
    send_notification(
        user_id=buyer,
        title=f'Cotação {rfq_number} aberta',
        message=f'Fornecedores já podem enviar propostas.',
        entity_type='rfq', entity_id=rfq_id, icon='📢',
    )
