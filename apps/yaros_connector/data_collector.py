import requests
from requests.exceptions import RequestException


class APIConnector:
    def __init__(self, url=None, publication=None, username=None, password=None):
        self.url = url
        self.publication = publication
        self.username = username
        self.password = password
        self.data = self.get_data()

    def get_categories_data(self):
        try:
            url = self.url + self.publication + 'categories/'
            request = requests.get(url, auth=(self.username, self.password))
            request.raise_for_status()
            return request.json()
        except RequestException as e:
            return f"Ошибка при получении данных категорий: {str(e)}"

    def get_products_data(self):
        try:
            url = self.url + self.publication + 'goods/'
            request = requests.get(url, auth=(self.username, self.password))
            request.raise_for_status()
            return request.json()
        except RequestException as e:
            return f"Ошибка при получении данных продуктов: {str(e)}"

    def get_data(self):
        data = {
            'categories': self.get_categories_data(),
            'products': self.get_products_data()
        }
        return data
