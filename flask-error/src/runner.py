import json
from datetime import datetime


def fetch_order_details(order_id):
    response = json.dumps({
        "order_id": order_id,
        "items": [
            {"sku": "WIDGET-42", "qty": 2, "price": 19.99},
            {"sku": "GADGET-7", "qty": 1, "price": 49.99},
        ],
        "customer": {"id": 12, "name": "Leander"},
        "status": "processing",
        "shipped_at": None,
    })
    return json.loads(response)


def error():
    order = fetch_order_details("ORD-20260212-1847")
    if order["shipped_at"] is not None:
        shipped_at = datetime.fromisoformat(order["shipped_at"])
        days_since_shipped = (datetime.now() - shipped_at).days
    else:
        # Order hasn't been shipped yet
        shipped_at = None
        days_since_shipped = None
