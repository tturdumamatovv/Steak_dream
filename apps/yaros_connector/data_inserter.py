from apps.yaros_connector.data_collector import APIConnector
from apps.yaros_connector.models import Supplier
import json
from apps.catalog.models import Category, Product
from django.db import transaction


class APIInserter:
    def __init__(self, supplier=Supplier):
        self.supplier = supplier
        self.data = APIConnector(
            url=supplier.url,
            publication=supplier.publication,
            username=supplier.username,
            password=supplier.password
        ).data

    def create(self):
        category_data = self.data.get('categories', {})
        if isinstance(category_data, str):
            category_data = json.loads(category_data)

        category_objects = []
        existing_category_ids = set(Category.objects.values_list('supplier_id', flat=True))
        for category in category_data.get('categories', []):
            if category['ID'] not in existing_category_ids:
                category_objects.append(Category(
                    supplier_id=category['ID'],
                    title=category['TITLE'],
                    sort_priority=category['SORT_PRIORITY'],
                    activity=category['ACTIVITY']
                ))

        Category.objects.bulk_create(category_objects)

        categories = {cat.supplier_id: cat for cat in Category.objects.all()}

        product_data = self.data.get('products', {})
        if isinstance(product_data, str):
            product_data = json.loads(product_data)

        existing_product_ids = set(Product.objects.values_list('supplier_id', flat=True))

        product_objects = []
        for product in product_data.get('goods', []):
            category = categories.get(product['CATEGORY_ID'])
            if category and product['ID'] not in existing_product_ids:
                try:
                    price = product['PRICES'][1]['PRICE']
                except IndexError:
                    price = product['PRICES'][0]['PRICE']
                except KeyError:
                    price = 0
                product_objects.append(Product(
                    supplier_integration=self.supplier,
                    supplier_id=product['ID'],
                    category=category,
                    title=product['TITLE'],
                    price=price,
                    quantity=float(product['QUANTITY']) if product['QUANTITY'] != '0' else 0.0,
                    image_url=product['IMAGE_URL'],
                    description=product['DESCRIPTION'],
                    measure=product['MEASURE'],
                    sort_priority=product['SORT_PRIORITY'],
                    activity=product['ACTIVITY']
                ))

        Product.objects.bulk_create(product_objects)

    def update_all_products(self):
        product_data = self.data.get('products', {})
        if isinstance(product_data, str):
            product_data = json.loads(product_data)

        product_ids = [prod['ID'] for prod in product_data.get('goods', [])]

        products_to_update = Product.objects.filter(supplier_id__in=product_ids).in_bulk(field_name='supplier_id')

        updated_products = []
        for product_info in product_data.get('goods', []):
            product = products_to_update.get(product_info['ID'])
            if product:
                try:
                    product.price = product_info['PRICES'][1]['PRICE'] if len(product_info['PRICES']) > 1 else \
                    product_info['PRICES'][0]['PRICE']
                except (IndexError, KeyError):
                    product.price = 0
                try:
                    product.quantity = float(product_info['QUANTITY'])
                except (ValueError, KeyError):
                    product.quantity = 0

                updated_products.append(product)

        Product.objects.bulk_update(updated_products, ['price', 'quantity'])


