import requests


class APIConnector:
    def __init__(self, url=None, publication=None, username=None, password=None):
        self.url = url
        self.publication = publication
        self.username = username
        self.password = password
        self.data = self.get_data()

    def get_categories_data(self):
        url = self.url + self.publication + 'categories/'
        request = requests.get(url, auth=(self.username, self.password))

        return request.text

    def get_products_data(self):
        url = self.url + self.publication + 'goods/'
        request = requests.get(url, auth=(self.username, self.password))

        return request.text

    def get_data(self):
        data = {
            'categories': self.get_categories_data(),
            'products': self.get_products_data()
        }
        return data
