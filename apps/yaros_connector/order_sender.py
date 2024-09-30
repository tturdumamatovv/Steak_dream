from apps.yaros_connector.models import Supplier
import requests
import json


class APIOrderSender:
    def __init__(self, supplier=Supplier, order=None):
        self.supplier = supplier
        self.url = self.supplier.url + self.supplier.publication + 'orders/'
        if order:
            self.prepare_order(order)

    def prepare_order(self, order):
        pass

    def send_order(self, order):
        # Формируем JSON-объект для отправки
        order_data = {
            "orders": [
                {
                    "id": order.id,
                    "type": order.type,
                    "infosystem": order.infosystem,
                    "date": order.date,
                    "status": order.status,
                    "pay_method": order.pay_method,
                    "change": order.change,
                    "total": order.total,
                    "user": {
                        "name": order.user.username,  # Предполагается, что у пользователя есть поле username
                        "phone": order.user.phone  # Предполагается, что у пользователя есть поле phone
                    },
                    "address": order.addresses.address,  # Предполагается, что у адреса есть поле address
                    "comment": order.comment,
                    "items": [
                        {
                            "product_id": item.product.id,  # Предполагается, что у продукта есть поле id
                            "quantity": str(item.quantity),
                            "price": str(item.amount / item.quantity),  # Предполагается, что amount делится на quantity
                            "amount": str(item.amount)
                        } for item in order.order_items.all()  # Предполагается, что у заказа есть связанные элементы
                    ]
                }
            ]
        }

        # Отправляем запрос на API
        response = requests.post(self.url, json=order_data)
        return response.json()  # Возвращаем ответ от API
