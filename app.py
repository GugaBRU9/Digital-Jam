import os
import pandas as pd
import datetime
import seaborn as sns
import matplotlib.pyplot as plt
from client import Client
from products import Products
from sales import Sales
pd.set_option('display.float_format', '{:.0f}'.format)

def clear_screen():
    """Clears the terminal screen for improved user interface clarity.

        This function uses operating system-specific commands to clear the console,
        ensuring a clean screen for subsequent output. This enhances user experience
        by preventing clutter and improving readability.
        """
    os.system('cls' if os.name == 'nt' else 'clear')
def end():
    """Terminates the application and clears the terminal screen.

       This function performs the necessary cleanup before application exit,
       including clearing the terminal screen and printing an exit message.
       """
    clear_screen()
    print('Ending the application')
def register_new_costumer():
    """Registers a new customer, collecting and storing their details.

        This function prompts the user for customer information such as first name,
        last name, email, and phone number. It then creates a new 'Client' object
        and adds it to the client list. A success message is displayed, and the
        new client's details are returned.

        Returns:
            dict: A dictionary containing the newly registered customer's information.
        """
    first_name = input('First name: ')
    last_name = input('Last name: ')
    email = input('E-mail: ')
    phone = input('Phone number: ')
    customer = Client(first_name, last_name, email, phone)
    customer.client_list()
    client = Client.get_client(customer._clientid)
    print(f'Costumer {first_name} successfully registered')
    input('Type any key to return: ')
    return client
def register_new_product():
    """Registers a new product, storing its details and calculating its price.

        This function collects product information, including name, desired profit
        percentage, cost, and quantity. It creates a 'Products' object, adds it to
        the product list, and displays a success message with the calculated price.
        """
    name = input('Product name: ')
    percent_profit = float(input('Desired profit percentage: '))
    cost = float(input('Product cost: '))
    qtd = int(input('How many products: '))
    product = Products(name, percent_profit, cost, qtd)
    product.product_list()
    print(f'Product {name} successfully registered with price {product.price}')
    input('Type any key to return: ')
def update_costumer():
    """Updates an existing customer's information based on their name.

        This function displays the current customer list and prompts the user to
        select a customer for update. It allows modification of email and phone
        number, updating the customer's record and displaying a success message.
        """
    df = pd.read_csv('client_list.csv')
    print(df.loc[:,['first_name', 'last_name', 'email', 'phone']].to_string(index=False))
    first_name = input('Type the costumer First name: ')
    last_name = input('Type the costumer Last name: ')
    clientid = Client.get_clientid(first_name,last_name)
    if clientid:
        client = Client.get_client(clientid)
        confirm_email = input(f'Want to change the {client['email']} email [Y/N]? ').lower()
        if confirm_email == 'y':
            email = input('Type the new email: ')
        else:
            email = None
        confirm_phone = input(f'Want to change the {client['phone']} email [Y/N]? ').lower()
        if confirm_phone == 'y':
            phone = input('Type the new phone: ')
        else:
            phone = None
        Client.update_client(first_name, last_name, email, phone)
        print(f'Costumer {first_name} successfully updated')
        input('Type any key to return: ')
    else:
        error('Costumer not found')
def update_product():
    """Updates an existing product's information based on its name.

        This function displays the current product list and prompts the user to
        select a product for update. It allows modification of profit percentage,
        cost, and quantity, updating the product's record and displaying a
        success message.
        """
    df = pd.read_csv("product_list.csv")
    print(df.loc[:, ['id', 'name', 'price']]
          .assign(price=df['price'].map('{:.2f}'.format))
          .to_string(index=False))
    name = input('Type the product name: ')
    productid = Products.get_productid(name)
    if productid:
        product = Products.get_product(productid)
        confirm_profit = input(f'Want to change the {product['profit']} percentage, current price {product['price']} [Y/N]? ').lower()
        if confirm_profit == 'y':
            profit = int(input('Type the new percentage: '))
            print(f'New price {product['price']}')
        else:
            profit = None
        confirm_cost = input(f'Want to change the {product['cost']} cost [Y/N]? ').lower()
        if confirm_cost == 'y':
            cost = float(input('Type the new cost: '))
        else:
            cost = None
        confirm_qtd = input(f'Want to change the {product['quantity']} quantity [Y/N]? ').lower()
        if confirm_qtd == 'y':
            qtd = int(input('Type the new quantity: '))
        else:
            qtd = None
        Products.update_products(productid, profit, cost, qtd)
        print(f'Product {name} successfully updated')
        input('Type any key to return: ')
    else:
        error('Product not found')
def delete_costumer():
    """Deletes a customer's record based on their name.

       This function displays the current customer list and prompts the user to
       select a customer for deletion. It removes the customer's record and
       displays a success message.
       """
    df = pd.read_csv('client_list.csv')
    print(df.loc[:, ['first_name', 'last_name', 'email', 'phone']].to_string(index=False))
    first_name = input('Type the costumer First name: ')
    last_name = input('Type the costumer Last name: ')
    clientid = Client.get_clientid(first_name, last_name)
    if clientid:
        Client.delete_client(clientid)
        print(f'Costumer {first_name} successfully deleted')
        input('Type any key to return: ')
    else:
        error('Costumer not found')
def delete_product():
    """Deletes a product's record based on its name.

       This function displays the current product list and prompts the user to
       select a product for deletion. It removes the product's record and
       displays a success message.
       """
    df = pd.read_csv("product_list.csv")
    print(df.loc[:, ['id', 'name', 'price']]
          .assign(price=df['price'].map('{:.2f}'.format))
          .to_string(index=False))
    name = input('Type the product name: ')
    productid = Products.get_productid(name)
    if productid:
        Products.delete_product(productid)
        print(f'Product {name} successfully deleted')
        input('Type any key to return: ')
    else:
        error('Product not found')
def account_check():
    """Verifies customer account existence and handles login or creation.

        This function checks if a customer has an existing account. If yes, it
        attempts to log them in. Otherwise, it prompts for account creation.

        Returns:
            dict: Customer details if login/creation is successful, None otherwise.
        """
    has_account = input('The costumer already has an account? [Y/N]: ').lower().strip()
    if has_account == 'y':
        first_name = input('Type the costumer First name: ')
        last_name = input('Type the costumer Last name: ')
        clientid = Client.get_clientid(first_name, last_name)
        client = Client.get_client(clientid)
        print('Log in successful')
        return client
    else:
        create_account = input('Do you want to create an account? [Y/N]: ').lower().strip()
        if create_account == 'y':
            client = register_new_costumer()
            return client
        else:
            return None
def add_to_cart(cart, product, client= None):
    """Adds a specified quantity of a product to the shopping cart.

        This function prompts the user to input the desired quantity of a product
        to add to the cart. It verifies if the requested quantity is available
        and applies a discount if the client is a premium member. The product
        name and its price are then appended to the cart dictionary.

        Args:
            cart (dict): The shopping cart dictionary containing product names and prices.
            product (dict): A dictionary containing product details, including name, price, and quantity.
            client (dict, optional): A dictionary containing client details. Defaults to None.

        Returns:
            dict: The updated shopping cart dictionary.
        """
    df = pd.read_csv('product_list.csv')
    while True:
        how_many = int(input(f'How many {product['name']} do you want to buy? '))
        if how_many <= product['quantity']:
            break
        else:
            print(f'The maximum number of {product['name']} available is {product['quantity']}')
    if client['level'] and client is not None:
        product['price'] = product['price'] * 0.9
    for c in range(how_many):
        cart['product'].append(product['name'])
        cart['price'].append(product['price'])
    return cart
def week_analysis():
    """Analyzes and visualizes sales data for the current week.

       This function reads sales data from a CSV file, processes it to extract
       weekday information, and generates visualizations of sales trends. It
       offers options to view sales per weekday, product sales per weekday,
       and a comparison with the previous week's sales.
       """
    df = pd.read_csv('sales_list.csv')
    df['datetime'] = pd.to_datetime(df['datetime'])
    df['week_day'] = df['datetime'].dt.strftime('%A')
    df['product_name'] = df['product'].apply(lambda x: Products.get_product(x)['name'])
    today = datetime.datetime.now()
    monday = today - pd.Timedelta(days= today.weekday())
    sunday = monday + pd.Timedelta(days = 6)
    monday = datetime.datetime.combine(monday, datetime.time.min)
    sunday = datetime.datetime.combine(sunday, datetime.time.max)
    week = df.loc[(df['datetime'] >= monday) & (df['datetime'] <= sunday)]
    week_sales_per_day = week['week_day'].value_counts().reset_index()
    show = input('Do you want to see the graphic of the sales per day of the week? [Y/N]').strip().lower()
    if show == 'y':
        sns.barplot(week_sales_per_day, x= 'week_day', y= 'count')
        plt.show()
    else:
        pass
    products_sales_per_week_day = df.groupby(df['week_day'])['product_name'].value_counts().reset_index()
    show = input('Do you want to see the graphic of the product sales per day? [Y/N]').strip().lower()
    if show == 'y':
        plt.figure(figsize=(16,9))
        sns.barplot(products_sales_per_week_day, x='week_day', y= 'count', hue= 'product_name')
        plt.show()
    else:
        pass
    show = input('Do you want to compare the sales of this week with the sales of the last week? [Y/N]').strip().lower()
    if show == 'y':
        last_week_monday = monday - pd.Timedelta(days=7)
        last_week_sunday = monday - pd.Timedelta(days=1)
        last_week = df.loc[(df['datetime'] >= last_week_monday) & (df['datetime'] <= last_week_sunday)]
        last_week_sales = last_week['week_day'].value_counts().reset_index()
        fig, axes = plt.subplots(1, 2, figsize=(12, 5))
        sns.barplot(last_week_sales, x= 'week_day', y= 'count', ax= axes[0])
        sns.barplot(week_sales_per_day, x='week_day', y= 'count', ax= axes[1])
        plt.tight_layout()
        plt.show()
    input('Type any key to return')
def month_analysis():
    """Analyzes and visualizes sales data for the current month.

        This function processes sales data to extract monthly and weekly trends,
        offering visualizations of product sales, weekly sales, and a comparison
        with the previous month's sales.
        """

    df = pd.read_csv('sales_list.csv')
    df['datetime'] = pd.to_datetime(df['datetime'])
    df['month'] = df['datetime'].dt.strftime('%B')
    df['product_name'] = df['product'].apply(lambda x: Products.get_product(x)['name'])
    df['week'] = df['datetime'].dt.strftime('%U')
    today = datetime.datetime.now()
    this_month = df.loc[df['month'] == today.strftime('%B')]
    show = input('Do you want to see the graphic of the product sales for this month? [Y/N]').strip().lower()
    if show == 'y':
        product_sales_this_month = this_month['product_name'].value_counts().reset_index()
        sns.barplot(product_sales_this_month, x='product_name', y='count')
        plt.show()
    else:
        pass
    sales_per_week = this_month['week'].value_counts().reset_index()
    show = input('Do you want to see the graphic of the sales per week of the month? [Y/N]').strip().lower()
    if show == 'y':
        sns.barplot(sales_per_week, x='week', y='count')
        plt.show()
    else:
        pass

    show = input('Do you want to compare the sales of this month with the sales of the month? [Y/N]').strip().lower()
    if show == 'y':
        if today.month != 1:
            date_last_month =datetime.datetime(today.year,today.month - 1, today.day)
        else:
            date_last_month =datetime.datetime(today.year - 1, 12, today.day)
        last_month = df.loc[df['month'] == date_last_month.strftime('%B')]
        sales_last_month = last_month['week'].value_counts().reset_index()
        fig, axes = plt.subplots(1,2, figsize= (12,5))
        sns.barplot(sales_per_week, x= 'week', y='count', ax= axes[1])
        sns.barplot(sales_last_month, x='week', y='count', ax= axes[0])
        plt.show()
def year_analysis():
    """Analyzes and visualizes sales data for the current year.

       This function processes sales data to extract yearly and monthly trends,
       offering visualizations of product sales, monthly sales, and a comparison
       with the previous year's sales.
       """
    df = pd.read_csv('sales_list.csv')
    df['datetime'] = pd.to_datetime(df['datetime'])
    df['year'] = df['datetime'].dt.strftime('%Y')
    df['product_name'] = df['product'].apply(lambda x: Products.get_product(x)['name'])
    df['month'] = df['datetime'].dt.strftime('%B')
    today = datetime.datetime.now()
    this_year = df.loc[df['year'] == today.strftime('%Y')]
    show = input('Do you want to see the graphic of the product sales for this year? [Y/N]').strip().lower()
    if show == 'y':
        product_sales_this_year = this_year['product_name'].value_counts().reset_index()
        sns.barplot(product_sales_this_year, x='product_name', y='count')
        plt.show()
    else:
        pass
    sales_per_month = this_year['month'].value_counts().reset_index()
    show = input('Do you want to see the graphic of the sales per week of the month? [Y/N]').strip().lower()
    if show == 'y':
        sns.barplot(sales_per_month, x='month', y='count')
        plt.show()
    else:
        pass

    show = input('Do you want to compare the sales of this month with the sales of the month? [Y/N]').strip().lower()
    if show == 'y':
        date_last_year = datetime.datetime(today.year - 1, today.month, today.day)
        last_month = df.loc[df['year'] == date_last_year.strftime('%Y')]
        sales_last_year = last_month['month'].value_counts().reset_index()
        fig, axes = plt.subplots(1, 2, figsize=(12, 5))
        sns.barplot(sales_per_month, x='month', y='count', ax=axes[1])
        sns.barplot(sales_last_year, x='month', y='count', ax=axes[0])
        plt.show()
def show_products(client=None):
    """Displays available products and prompts for product selection.

       This function reads product data from a CSV file, applies a discount if
       the client is a premium member, and displays the product list. It then
       prompts the user to select a product by ID, validates the input, and
       returns the selected product's details.

       Args:
           client (dict, optional): Client details for discount application. Defaults to None.

       Returns:
           dict: Details of the selected product.
       """
    df = pd.read_csv('product_list.csv')
    if client['level'] and client is not None:
        df = df.assign(price= df['price'] * 0.9)
    print(df.loc[df['quantity'] != 0, ['id', 'name', 'price']]
          .assign(price=df['price'].map('{:.2f}'.format))
          .to_string(index=False))
    while True:
        productid = int(input('Type the ID of the chosen product: '))
        if productid in df['id'].values:
            product = Products.get_product(productid)
            break
        else:
            print('Please try again')

    return product
def sales_analytics():
    """Provides sales analysis options and visualizes sales data.

       This function presents a menu of sales analysis options, including weekly,
       monthly, and yearly analysis. It calls corresponding analysis functions
       based on user input and handles potential errors.
       """
    while True:
        clear_screen()
        print('Sales page')
        print('''
           1. Week analysis 
           2. Month analysis
           3. Year analysis 
           4. Return to start selling
           
           ''')

        try:
            chosen_option = int(input('Chose your option: '))
            if chosen_option == 1:
                week_analysis()
            elif chosen_option == 2:
                month_analysis()
            elif chosen_option == 3:
                year_analysis()
            elif chosen_option == 4:
                break
            else:
                print('Please teype a positive integer number!')
                error()

        except Exception as e:
            print(f'Wrong type please chose between the given options: {e}')
            error()
            pass
def remove_from_cart(cart, product):
    """Removes a specified product from the shopping cart.

       This function iterates through the shopping cart to find and remove
       the specified product.

       Args:
           cart (dict): The shopping cart dictionary.
           product (str): The name of the product to remove.
       """
    for c, k in enumerate(cart['product']):
        if k == product:
            cart['product'].pop(c)
            cart['price'].pop(c)
            break
def checkout(cart,client):
    """Processes the checkout, calculating total cost and updating records.

       This function displays the cart contents, allows item removal, calculates
       the total cost, updates sales and client records, and handles client
       level upgrades.

       Args:
           cart (dict): The shopping cart dictionary.
           client (dict, optional): Client details for record updates. Defaults to None.
       """
    while True:
        cart = pd.DataFrame(cart)
        print(cart['product'].value_counts().to_string(header= False))
        cart = cart.to_dict(orient= 'list')
        remove = input('Do you want to remove any item? [Y/N]').lower().strip()
        if remove == 'y':
            product = input('Type the product name: ').title().strip()
            remove_from_cart(cart, product)
        elif remove == 'n':
            break
        else:
            print('Please type [Y] or [N]')
    amount_spent = sum(cart['price'])
    print(f'Total value: {amount_spent}')
    for c in cart['product']:
        if client is not None:
            sales = Sales(Products.get_productid(c), client['id'])
        else:
            sales = Sales(Products.get_productid(c), client)
        sales.sales_list()
        Products.sold(Products.get_productid(c))
    if client is not None:
        Client.client_purchase(client['id'])
        Client.amount_spent(client['id'], amount_spent)
        print(f'Current level {Client.level(client['id'])}')
        if client['purchase'] >= 10 and client['amount_spent'] >= 1000 and not client['level']:
            Client.upgrade_level(client['id'])
            print(f'Congratulations you upgraded your level to {Client.level(client['id'])}')
    else:
        pass
    input('Order finished type any key to return: ')
def make_an_order():
    """Facilitates the process of making a new order.

        This function handles the entire order process, from client account
        verification to checkout. It prompts the user to select products,
        adds them to the cart, and finalizes the order.
        """
    client = account_check()
    cart = {'product': [],
            'price': []}
    while True:
        clear_screen()
        print('Products')
        product = show_products(client)
        cart = add_to_cart(cart, product, client)
        stop = input('Want to stop ordering? [Y/N]').lower().strip()
        if stop == 'y':
            break
        else:
            pass
    checkout(cart,client)

def start_selling():
    """Provides the main sales interface and navigation.

        This function presents the user with a menu of sales-related options,
        including making an order and accessing sales analytics. It handles
        user input and calls the corresponding functions.
        """
    while True:
        clear_screen()
        print('Sales page')
        print('''
        1. Make an order   
        2. Sales analytics 
        3. Back to main menu 
        ''')

        try:
            chosen_option = int(input('Chose your option: '))
            if chosen_option == 1:
                make_an_order()
            elif chosen_option == 2:
                sales_analytics()
            elif chosen_option == 3:
                break
            else:
                print('Please teype a positive integer number!')
                error()

        except Exception as e:
            print(f'Wrong type please chose between the given options: {e}')
            error()
            pass

def error(text=''):
    """Displays an error message and prompts for user confirmation.

      This function displays an error message to the user and waits for
      user input before returning to the previous menu.

      Args:
          text (str, optional): Additional error details. Defaults to ''.
      """
    print(f'Ops! An error happened {text}')
    input('Type any key to return: ')

def product_menu():
    """Manages product-related operations through a menu interface.

        This function presents a menu of product management options, including
        registering, updating, and deleting products. It handles user input
        and calls the corresponding functions.
        """
    while True:
        clear_screen()
        print('SmartData')
        print('''
        1. Register new product  
        2. Update product data
        3. Delete product 
        4. Back to main menu 
        ''')

        try:
            chosen_option = int(input('Chose your option: '))
            if chosen_option == 1:
                register_new_product()
            elif chosen_option == 2:
                update_product()
            elif chosen_option == 3:
                delete_product()
            elif chosen_option == 4:
                break
            else:
                print('Please teype a positive integer number!')
                error()

        except Exception as e:
            print(f'Wrong type please chose between the given options: {e}')
            error()
            pass

def costumer_menu():
    """Manages customer-related operations through a menu interface.

        This function presents a menu of customer management options, including
        registering, updating, and deleting customers. It handles user input
        and calls the corresponding functions.
        """
    while True:
        clear_screen()
        print('SmartData')
        print('''
        1. Register new costumer  
        2. Update costumer data
        3. Delete costumer 
        4. Back to main menu 
        ''')

        try:
            chosen_option = int(input('Chose your option: '))
            if chosen_option == 1:
                register_new_costumer()
            elif chosen_option == 2:
                update_costumer()
            elif chosen_option == 3:
                delete_costumer()
            elif chosen_option == 4:
                break
            else:
                print('Please teype a positive integer number!')
                error()

        except Exception as e:
            print(f'Wrong type please chose between the given options: {e}')
            error()
            pass
def main():
    """Provides the main application menu and navigation.

        This function presents the user with the main menu, offering options
        to manage customers, products, start selling, or exit the application.
        It handles user input and calls the corresponding functions.
        """
    while True:
        clear_screen()
        print('SmartData')
        print('''
        1. Customer menu 
        2. Product menu 
        3. Start selling
        4. Exit
        ''')

        try:
            chosen_option = int(input('Chose your option: '))
            if chosen_option == 1:
                costumer_menu()
            elif chosen_option == 2:
                product_menu()
            elif chosen_option == 3:
                start_selling()
            elif chosen_option == 4:
                end()
                break
            else:
                print('Please type a positive integer number!')
                error()

        except:
            print('Wrong type please chose between the given options ')
            error()
            pass


if __name__ == '__main__':
    main()
