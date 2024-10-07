import requests
import json
from datetime import datetime


class APIOrderSender:
    def __init__(self, supplier, order=None):
        self.supplier = supplier
        self.url = str(self.supplier.url) + str(self.supplier.publication) + 'orders/'
        self.infosystem = self.supplier.infosystem
        self.username = self.supplier.username
        self.password = self.supplier.password
        if order:
            self.prepare_order(order)

    def prepare_order(self, order):
        items = order.order_items.all()
        item_data = []
        for item in items:
            item_price = item.amount / item.quantity if item.quantity else 0
            item_data.append({
                "product_id": str(item.product.supplier_id),
                "quantity": "{:.2f}".format(item.quantity),
                "price": "{:.2f}".format(item_price),
                "amount": "{:.2f}".format(item.amount)
            })

        timestamp = int(order.created_at.timestamp())
        order_data = {
            "orders": [
                {
                    "id": order.id,
                    "type": order.type,
                    "infosystem": self.infosystem,
                    "date": str(timestamp),
                    "status": order.status,
                    "pay_method": order.pay_method,
                    "change": "{:.2f}".format(order.change),
                    "total": "{:.2f}".format(order.total),
                    "user": {
                        "name": order.user.full_name,
                        "phone": order.user.phone_number
                    },
                    "address": order.addresses.city,
                    "comment": order.comment,
                    "items": item_data
                }
            ]
        }

        self.send_order(order_data)

    def send_order(self, order_data):
        headers = {
            'Cache-Control': 'no-cache',
            'Content-Type': 'application/json',
            'User-Agent': 'CustomUserAgent/1.0',
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive'
        }
        response = requests.post(self.url, json=order_data, headers=headers, auth=(self.username, self.password))
        return response.text
