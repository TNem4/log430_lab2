"""
Orders (read-only model)
SPDX - License - Identifier: LGPL - 3.0 - or -later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""

import json

from db import get_sqlalchemy_session, get_redis_conn
from models.order_item import OrderItem
from sqlalchemy import desc
from models.order import Order

def get_order_by_id(order_id):
    """Get order by ID from Redis"""
    r = get_redis_conn()
    return r.hgetall(order_id)

def get_orders_from_mysql(limit=9999):
    """Get last X orders"""
    session = get_sqlalchemy_session()
    return session.query(Order).order_by(desc(Order.id)).limit(limit).all()

def get_orders_from_redis(limit=9999):
    """Get last X orders"""
    r = get_redis_conn()

    keys = list(r.scan_iter(match="order:*"))

    keys.sort(key=lambda x: int(x.split(':')[1]), reverse=True)
    keys = keys[:limit]

    orders = []
    for key in keys:
        order_data = r.hgetall(key)


        order_data["order_id"] = int(order_data["order_id"])
        order_data["user_id"] = int(order_data["user_id"])
        order_data["total_amount"] = float(order_data["total_amount"])
        order_data["order_items"] = json.loads(order_data["order_items"])

        order = Order(id=order_data["order_id"], user_id=order_data["user_id"], total_amount=order_data["total_amount"], 
                      order_items=[OrderItem(product_id=item["product_id"], quantity=item["quantity"], unit_price=item["unit_price"]) for item in order_data["order_items"]])
        orders.append(order)

    return orders

def get_highest_spending_users():
    """Get report of best selling products"""
    # TODO: écrivez la méthode
    # triez le résultat par nombre de commandes (ordre décroissant)
    return []