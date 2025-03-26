import datetime
from products import Products
from client import Client

class Sales:
    """Represents a sales transaction in the store.
       This class stores details about a product sale, including the product sold,
       the client (if applicable), the sale timestamp, cost, price, and profit.
       It also manages the recording of sales transactions in a CSV file.
       Attributes:
           _product (int): The ID of the product sold.
           _time (datetime): The timestamp of the sale.
           _client (int or None): The ID of the client who made the purchase, or None for anonymous sales.
           _cost (float): The cost of the product.
           _price (float): The price at which the product was sold, considering possible discounts.
           _profit (float): The profit earned from the sale.
       """
    def __init__(self,product,client=None):
        """Initializes a Sales object with the given product and client.
               The price is determined based on whether the client is eligible for
               a discount (VIP status).
               Args:
                   product (int): The ID of the product being sold.
                   client (int or None, optional): The ID of the client making the purchase. Defaults to None.
               """
        self._product = product
        self._time = datetime.datetime.now()
        self._client = client
        self._cost = Products.get_product(product)['cost']
        self._price = Products.get_product(product)["price"] if client is None or not Client.get_client(client)['level'] else Products.get_product(product)['price'] * 0.9
        self._profit = self._price - self._cost
    def sales_list(self):
        """Records the sale in the sales list CSV file.
               If the file does not exist, it creates it and adds the necessary headers.
               The new sale entry is then appended to the file.
               Returns:
                   None
               """
        import csv
        import pandas as pd
        try:
            with open('sales_list.csv', mode='x', newline='', encoding='utf-8') as archive:
                writer = csv.writer(archive)
                writer.writerow(['client', 'product', 'datetime', 'cost', 'price', 'profit'])
        except FileExistsError:
            pass
        file = pd.read_csv('sales_list.csv')

        dict = {
            'client': [self._client],
            'product': [self._product],
            'datetime': [self._time],
            'cost': [self._cost],
            'price': [self._price],
            'profit': [self._profit]
        }
        df = pd.DataFrame(dict)
        file = file.dropna(axis= 1, how= 'all')
        df = df.dropna(axis= 1, how= 'all')
        df = pd.concat([file,df], ignore_index= True)
        return df.to_csv('sales_list.csv', index=False)
