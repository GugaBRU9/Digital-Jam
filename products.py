from id import create_id
from client import Client
class Products:
    """Manages product information and operations.

       This class provides methods to initialize, store, update, retrieve,
       and delete product data. It also includes functionality to calculate
       product prices and handle sales transactions.
       """
    def __init__(self, name, percent_profit, cost, quantity):
        """Initializes a new product instance.

               Args:
                   name (str): The name of the product.
                   percent_profit (float): The profit percentage.
                   cost (float): The cost of the product.
                   quantity (int): The initial quantity of the product.
               """
        self._productid = create_id('product_list.csv',5)
        self._name = name.title().strip()
        self._cost = cost
        self._quantity = quantity
        self._profit = percent_profit/100
        self._price = cost * (1 + self._profit)
    def product_list(self):
        """Stores product information in a CSV file.

               This method creates or appends product data to 'product_list.csv',
               including product ID, name, price, cost, quantity, and profit.
               """
        import csv
        try:
            with open('product_list.csv', mode='x', newline='', encoding='utf-8') as archive:
                writer = csv.writer(archive)
                writer.writerow(['id','name', 'price', 'cost', 'quantity', 'profit'])
        except FileExistsError:
            pass

        with open('product_list.csv', mode='a', newline='', encoding='utf-8') as archive:
            writer = csv.writer(archive)
            writer.writerow ([self._productid, self._name, self._price, self._cost, self._quantity, self._profit])
    @classmethod
    def update_products(cls, id, new_price= None, new_cost= None, new_quantity= None, ):
        """Updates product information in the CSV file.

               Args:
                   id (int): The ID of the product to update.
                   new_price (float, optional): The new price of the product. Defaults to None.
                   new_cost (float, optional): The new cost of the product. Defaults to None.
                   new_quantity (int, optional): The new quantity of the product. Defaults to None.

               Returns:
                   None: Updates the CSV file directly.
               """
        import pandas as pd
        df = pd.read_csv('product_list.csv')
        df.loc[df['id'] == id,'price'] = new_price if new_price else df.loc[df['id'] == id,'price']
        df.loc[df['id'] == id, 'cost'] = new_cost if new_cost else df.loc[df['id'] == id, 'cost']
        df.loc[df['id'] == id, 'quantity'] = new_quantity if new_quantity else df.loc[df['id'] == id, 'quantity']
        return df.to_csv('product_list.csv', index=False)
    @classmethod
    def get_product(self,id):
        """Retrieves product information based on its ID.

               Args:
                   id (int): The ID of the product to retrieve.

               Returns:
                   dict: A dictionary containing the product's details.
               """
        import pandas as pd
        df = pd.read_csv('product_list.csv')
        product = df.loc[df['id'] == id]
        product_dict = product.to_dict(orient= 'records')[0]
        return product_dict
    @classmethod
    def sold(cls,id):
        """Updates product quantity after a sale.

               Args:
                   id (int): The ID of the sold product.

               Returns:
                   None: Updates the CSV file directly.
               """
        import pandas as pd
        df = pd.read_csv('product_list.csv')
        value = df.loc[df['id'] == id, ['quantity']]
        value = value.iloc[0] if not value.empty else None
        if value is None:
            pass
        else:
            value = value.squeeze()
            value = int(value)
        df.loc[df['id'] == id, ['quantity']] = value - 1
        return df.to_csv('product_list.csv', index= False)

    @classmethod
    def get_productid(cls, name):
        """Retrieves product ID based on its name.

                Args:
                    name (str): The name of the product.

                Returns:
                    int: The ID of the product, or None if not found.
                """
        import pandas as pd
        df = pd.read_csv('product_list.csv')
        productid = df.loc[df['name'] == name.title().strip(), ['id']]
        productid = productid.iloc[0] if not productid.empty else None
        if productid is None:
            pass
        else:
            productid = productid.squeeze()
            productid = int(productid)
        return productid
    @classmethod
    def delete_product(cls, productid):
        """Deletes a product from the CSV file based on its ID.

               Args:
                   productid (int): The ID of the product to delete.

               Returns:
                   None: Updates the CSV file directly.
               """
        import pandas as pd
        df = pd.read_csv('product_list.csv')
        if productid not in df['id'].values:
            return None
        else:
            df = df.loc[df['id'] != productid]
            return df.to_csv('product_list.csv', index=False)
    @property
    def price(self):
        """Retrieves the product's price.

               Returns:
                   float: The price of the product.
               """
        return self._price