import requests
import json
from apps.catalog.models import Product  # Импортируем модель Product


class ProductUpdater:
    def __init__(self, supplier):
        self.url = str(supplier.url) + str(supplier.publication) + 'goods/'
        self.username = supplier.username
        self.password = supplier.password

    def update_product_data(self, prod_ids):
        # Формируем URL с параметрами для получения продуктов по ID
        ids_param = ','.join(prod_ids)  # Преобразуем список ID в строку
        url = f"{self.url}?prodID={ids_param}"  # Формируем URL с параметром prodID
        response = requests.get(url, auth=(self.username, self.password))
        
        if response.status_code != 200:
            return f"Error fetching products: {response.text}"

        product_data = response.json().get('goods', [])
        existing_product_ids = set(Product.objects.values_list('supplier_id', flat=True))

        products_to_update = []
        for product_info in product_data:
            if product_info['ID'] in prod_ids:  # Проверяем, есть ли ID в переданном списке
                if product_info['ID'] in existing_product_ids:
                    product = Product.objects.get(supplier_id=product_info['ID'])
                    try:
                        product.price = product_info['PRICES'][1]['PRICE'] if len(product_info['PRICES']) > 1 else \
                        product_info['PRICES'][0]['PRICE']
                    except (IndexError, KeyError):
                        product.price = 0
                    try:
                        product.quantity = float(product_info['QUANTITY'])
                    except (ValueError, KeyError):
                        product.quantity = 0

                    products_to_update.append(product)

        # Обновляем только те продукты, которые были изменены
        Product.objects.bulk_update(products_to_update, ['price', 'quantity'])
        return f"Updated {len(products_to_update)} products."
