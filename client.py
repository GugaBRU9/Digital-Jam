from id import create_id
import pandas as pd
class Client:
    """
       Represents a client in the store system.
       Attributes:
           _clientid (int): Unique client identifier.
           _first_name (str): First name of the client.
           _last_name (str): Last name of the client.
           _email (str): Client's email address.
           _phone (str): Client's phone number.
           _purchase (int): Number of purchases made by the client.
           _spent (float): Total amount spent by the client.
           _level (bool): VIP status of the client (True if VIP, False otherwise).
       """
    def __init__(self, first_name, last_name, email, phone):
        """
              Initializes a new client with provided information.
              Args:
                  first_name (str): First name of the client.
                  last_name (str): Last name of the client.
                  email (str): Email address of the client.
                  phone (str): Phone number of the client.
              """
        self._clientid = create_id('client_list.csv',9)
        self._first_name = first_name.title().strip()
        self._last_name = last_name.title().strip()
        self._email = email
        self._phone = phone
        self._purchase = 0
        self._spent = 0
        self._level = False

    def client_list(self):
        """
               Adds the client to the client list CSV file. Creates the file if it doesn't exist.
               """
        import csv
        try:
            with open('client_list.csv', mode='x', newline='', encoding='utf-8') as archive:
                writer = csv.writer(archive)
                writer.writerow(['id', 'first_name', 'last_name', 'email', 'phone','purchase', 'amount_spent', 'level'])
        except FileExistsError:
            pass

        with open('client_list.csv', mode='a', newline='', encoding='utf-8') as archive:
            writer = csv.writer(archive)
            writer.writerow([self._clientid, self._first_name, self._last_name, self._email, self._phone, self._purchase, self._spent, self._level])
    @classmethod

    def update_client(cls, first_name, last_name, new_email=None, new_phone=None):
        """
                Updates the email and/or phone number of an existing client.
                Args:
                    first_name (str): First name of the client.
                    last_name (str): Last name of the client.
                    new_email (str, optional): New email address. Defaults to None.
                    new_phone (str, optional): New phone number. Defaults to None.
                """
        df = pd.read_csv('client_list.csv')
        clientid = Client.get_clientid(first_name,last_name)
        df.loc[df['id'] == clientid, 'email'] = new_email if new_email else df.loc[df['id'] == clientid, 'email']
        df.loc[df['id'] == clientid, 'phone'] = new_phone if new_phone else df.loc[df['id'] == clientid, 'phone']
        return df.to_csv('client_list.csv', index=False)
    @classmethod
    def get_clientid(cls,first_name,last_name):
        """
                Retrieves the client ID based on their first and last name.
                Args:
                    first_name (str): First name of the client.
                    last_name (str): Last name of the client.

                Returns:
                    int: Client ID if found, else None.
                """
        df = pd.read_csv('client_list.csv')
        clientid = df.loc[(df['first_name'] == first_name.title().strip()) & (df['last_name'] == last_name.title().strip()),['id']]
        clientid = clientid.iloc[0] if not clientid.empty else None
        if clientid is None:
            pass
        else:
            clientid = clientid.squeeze()
            clientid = int(clientid)
        return clientid
    @classmethod
    def get_client(cls, clientid):
        """
                Retrieves client details based on their ID.
                Args:
                    clientid (int): Client ID.
                Returns:
                    dict: Client details.
                """
        df = pd.read_csv('client_list.csv')
        client = df.loc[df['id'] == clientid]
        client_dict = client.to_dict(orient='records')[0]
        return client_dict
    @classmethod
    def client_purchase(cls,clientid):
        """
               Increments the purchase count of a client by 1.
               Args:
                   clientid (int): Client ID.
               """
        df = pd.read_csv('client_list.csv')
        purchase_value = df.loc[df['id'] == clientid, ['purchase']]
        purchase_value = purchase_value.iloc[0] if not purchase_value.empty else None
        if clientid is not None:
            purchase_value = purchase_value.squeeze()
            df.loc[df['id'] == clientid, ['purchase']] = int(purchase_value) + 1
        else:
            pass
        return df.to_csv('client_list.csv', index= False)
    @classmethod
    def amount_spent(cls,clientid, amount):
        """
               Adds an amount to the total spent by a client.
               Args:
                   clientid (int): Client ID.
                   amount (float): Amount spent in the new transaction.
               """
        df = pd.read_csv('client_list.csv')
        spent_value = df.loc[df['id'] == clientid, ['amount_spent']]
        spent_value = spent_value.iloc[0] if not spent_value.empty else None
        if clientid is not None:
            spent_value = spent_value.squeeze()
            df.loc[df['id'] == clientid, ['amount_spent']] = float(spent_value) + amount
        else:
            pass
        return df.to_csv('client_list.csv', index=False)
    @classmethod
    def delete_client(cls,clientid):
        """
                Deletes a client from the database.
                Args:
                    clientid (int): Client ID.
                """
        df = pd.read_csv('client_list.csv')
        if clientid not in df['id'].values:
            return None
        else:
            df = df.loc[df['id'] != clientid]
            return df.to_csv('client_list.csv', index=False)
    @classmethod
    def level(cls,clientid):
        """
               Retrieves the level of a client.
               Args:
                   clientid (int): Client ID.
               Returns:
                   str: 'VIP' if the client is VIP, else 'Normal'.
               """
        client = Client.get_client(clientid)
        level = client['level']
        return 'VIP' if level else 'Normal'
    @classmethod
    def upgrade_level(cls,clientid):
        """
             Upgrades a client to VIP level.
             Args:
                 clientid (int): Client ID.
             """
        df = pd.read_csv('client_list.csv')
        df.loc[df['id'] == clientid, ['level']] = True
        return df.to_csv('client_list.csv', index=False)
