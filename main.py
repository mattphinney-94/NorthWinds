import pymysql
import cryptography

def add_customer(cursor, conn):
    print('Provide the following user information...')
    # Prompt user for customer info
    comp = input('Company: ')
    lName = input('Last name: ')
    fName = input('First name: ')
    email = input('E-mail address: ')
    title = input('Job title: ')
    bPhone = input('Business phone number: ')
    hPhone = input('Home phone number: ')
    mPhone = input('Mobile phone number: ')
    fax = input('Fax: ')
    address = input('Address: ')
    city = input('City: ')
    state = input('State: ')
    zipCode = input('Zip code: ')
    country = input('Country: ')
    web = input('Web: ')
    notes = input('Notes: ')
    att = input('Attachments: ')

    # Handle NULLs
    varList = [comp, lName, fName, email, title, bPhone, hPhone, mPhone, fax, address, city, state, zipCode, country, web, notes, att]

    varList = [v.strip() or None for v in varList]

    # Attempt to add the new customer to the database
    try:
        cursor.execute(
            "INSERT INTO Customers (Company, LastName, FirstName, Email, JobTitle, BusinessPhone, HomePhone, MobilePhone,"
            "Fax, Address, City, State, ZIP, Country, Web, Notes, Attachments) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            varList
        )
        conn.commit()
        print("Customer added!")

    # Handle exceptions
    except Exception as e:
        conn.rollback()
        print("Error:", e)

# THE ADD ORDER FUNCTION STILL NEEDS WORK
def add_order(cursor, conn):
    print('Provide the following order information...')

    # For orders table
    eid = input('Employee ID: ')
    cid = input('Customer ID: ')
    oDate = input('Order date: ')
    sid = input('Shipper ID: ')
    sName = input('Shipper name: ')
    sAddress = input('Shipper address: ')
    sCity = input('Shipper city: ')
    sState = input('Shipper state: ')
    sZip = input('Shipper zip: ')
    sCountry = input('Shipper country: ')
    tax = '0'
    paymentType = input('Payment type: ')
    paidDate = input('Paid date: ')
    notes = input('Notes: ')
    taxRate = input('Tax rate: ')
    taxStatus = input('Tax status: ')
    statusid = '0'

    # For order details table
    oid = input('Order ID: ') # NOPE this is obtained from orders table
    pid= input('Product ID: ')
    q = input('Quantity: ')
    uPrice = input('Unit price: ')
    discount = input('Discount: ')

    # Handle NULLs
    varList = [eid, cid, oDate, sDate, sid, sName, sAddress, sCity, sState, sZip, sCountry, shipFee, tax, paymentType,
               paidDate, notes, taxRate, taxStatus, statusid]

    varList = [v.strip() or None for v in varList]

    # Attempt to add the new customer to the database
    try:
        cursor.execute(
            "INSERT INTO orders (EmployeeID, CustomerID, OrderDate, ShippedDate, ShipperID, ShipName,"
            "ShipAddress, ShipCity, ShipState, ShipZIP, ShipCountry, ShippingFee, Taxes, PaymentType, PaidDate, "
            "Notes, TaxRate, TaxStatus, StatusID)"
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            varList
        )
        conn.commit()
        print("Order added!")

    # Handle exceptions
    except Exception as e:
        conn.rollback()
        print("Error:", e)

def remove_order(cursor, conn):
    # Prompt user for order ID
    orderid = input('Provide the order ID of the order to be deleted: ')

    # Attempt to delete the order from both the orders and order_details tables, using a transaction
    try:
        conn.begin()

        cursor.execute(
            "DELETE FROM order_details WHERE OrderID IN(%s)", orderid
        )

        cursor.execute(
            "DELETE FROM orders WHERE OrderID IN(%s)", orderid
        )

        conn.commit()
        print("Order deleted.")

    # Handle exceptions
    except Exception as e:
        conn.rollback()
        print("Error:", e)

def ship_order(cursor, conn):
    orderid = input('Provide the order ID of the order to be shipped: ')

    # Check that there is no out of stock inventory
    cursor.execute('SELECT ProductID, Quantity FROM order_details WHERE OrderID = %s', (orderid,))
    productsCounts = cursor.fetchall()

    noOutOfStock = True

    for item in productsCounts:
        cursor.execute('SELECT TransactionType, Quantity FROM inventory_transactions WHERE ProductID = %s', (str(item[0]),))
        transactions = cursor.fetchall()

        inventory = 0

        for transaction in transactions:
            print(transaction)
            if transaction[0] == 1:
                inventory += transaction[1]
            else:
                inventory -= transaction[1]

        if inventory < item[1]:
            noOutOfStock = False
            print('Net inventory for ' + str(item[0]) + ' is ' + str(inventory))
            #break

    if noOutOfStock:
        # Get shipping info from the user
        shippingDate = input('Date shipped: ')
        shipperid = input('Shipper ID: ')
        shippingFee = input('Shipping fee: ')

        # Handle NULLs
        varList = [shippingDate, shipperid, shippingFee, orderid]

        varList = [v.strip() or None for v in varList]

        try:
            conn.begin()

            cursor.execute('UPDATE orders '
                           'SET ShippedDate = %s, ShipperID = %s, ShippingFee = %s '
                           'WHERE OrderID = %s;', varList)

            for item in productsCounts:
                values = ('1', str(item[0]), str(item[1]))
                cursor.execute('INSERT INTO inventory_transactions(TransactionType, TransactionCreatedDate, '
                               'TransactionModifiedDate, ProductID, Quantity) '
                               'VALUES(s%, NOW(), NOW(), s%, s%);', values)

            conn.commit()

        # Handle exceptions
        except Exception as e:
            conn.rollback()
            print("Error:", e)

        print('Order updated.')

    else:
        print('There is not enough quantity to fulfill this order.')

def show_pending_orders(cursor, conn):
    cursor.execute("""
        SELECT OrderID, CustomerID, EmployeeID, OrderDate,
               ShipName, ShipCity, ShipState, ShippingFee, StatusID
        FROM orders
        WHERE ShippedDate IS NULL
        ORDER BY OrderDate DESC;
    """)

    rows = cursor.fetchall()

    # Header
    print("=" * 110)
    print(f"{'OrderID':<10}{'CustID':<10}{'EmpID':<10}{'OrderDate':<20}"
          f"{'ShipName':<20}{'City':<15}{'State':<10}{'Fee':<10}{'Status':<10}")
    print("=" * 110)

    # Rows
    for row in rows:
        order_id = row[0]
        cust_id = row[1]
        emp_id = row[2]
        order_date = str(row[3]) if row[3] else "N/A"
        ship_name = (row[4][:17] + '...') if row[4] and len(row[4]) > 20 else (row[4] or "N/A")
        city = row[5] if row[5] else "N/A"
        state = row[6] if row[6] else "N/A"
        fee = row[7] if row[7] is not None else "N/A"
        status = row[8] if row[8] is not None else "N/A"

        print(f"{order_id:<10}{cust_id:<10}{emp_id:<10}{order_date:<20}"
              f"{ship_name:<20}{city:<15}{state:<10}{fee:<10}{status:<10}")

    print("=" * 110)

def add_transaction(cursor, conn):
    # Get transaction info from user
    print('Input details about the transaction...')
    print()
    tranType = input('TransactionType: ')
    while not tranType.isdigit() or int(tranType) < 1 or int(tranType) > 3:
        tranType = input('Enter an integer between 1 and 4: ')
    productid = input('Product ID: ')
    quantity = input('Quantity: ')
    pid = input('Purchase order ID: ')
    cid = input('Customer order ID: ')
    com = input('Comments: ')

    # Handle NULLs
    varList = [tranType, productid, quantity, pid, cid, com]

    varList = [v.strip() or None for v in varList]

    try:
        cursor.execute(
            'INSERT INTO inventory_transactions(TransactionType, TransactionCreatedDate, TransactionModifiedDate, ProductID, '
            'Quantity, PurchaseOrderID, CustomerOrderID, Comments) VALUES (%s, NOW(), NOW(), %s, %s, %s, %s, %s)',
            varList
        )

        conn.commit()

        print('Transaction added.')
        print()

    # Handle exceptions
    except Exception as e:
        conn.rollback()
        print("Error:", e)


def top_5_products(cursor, conn):
    cursor.execute("""
        SELECT p.ProductName, SUM(it.Quantity) AS total_sold
        FROM inventory_transactions it
        JOIN products p ON it.ProductID = p.ID
        WHERE it.TransactionType = 2
        GROUP BY it.ProductID, p.ProductName
        ORDER BY total_sold DESC
        LIMIT 5;
    """)

    rows = cursor.fetchall()

    print("=" * 50)
    print(f"{'Product':<30}{'Total Sold':<15}")
    print("=" * 50)

    for name, total in rows:
        print(f"{name:<30}{total:<15}")

    print("=" * 50)

def sub_menu(cursor, conn):
    # Initialize selection
    selection = 1

    while int(selection) != 3:
        print('Additional options: ')
        print('1. Add transaction')
        print('2. List the top 5 selling products')
        print('3. Return to main menu')


        # Get users selection and validate input
        selection = input('Select: ')
        while not selection.isdigit() or int(selection) < 1 or int(selection) > 3:
            selection = input('Please enter a number between 1 and 3: ')

        if selection == '1':
            add_transaction(cursor, conn)
        if selection == '2':
            top_5_products(cursor, conn)

def main():
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='CedarPoint2026!?',
        database='northwind'
    )

    cursor = conn.cursor()

    # Initialize selection so menu loop activates
    selection = 1

    # Print menu options
    while int(selection) != 7:
        print('1. Add customer')
        print('2. Add order')
        print('3. Remove order')
        print('4. Ship order')
        print('5. Print pending orders')
        print('6. More options')
        print('7. Exit')

        # Get users selection and validate input
        selection = input('Select: ')
        while not selection.isdigit() or int(selection) < 1 or int(selection) > 7:
            selection = input('Please enter a number between 1 and 7: ')

        # Call the appropriate function, based on user input
        if selection == '1':
            add_customer(cursor, conn)
        elif selection == '2':
            add_order(cursor, conn)
        elif selection == '3':
            remove_order(cursor, conn)
        elif selection == '4':
            ship_order(cursor, conn)
        elif selection == '5':
            show_pending_orders(cursor, conn)
        elif selection == '6':
            sub_menu(cursor, conn)

    cursor.execute('SELECT * FROM customers LIMIT 5')

    rows = cursor.fetchall()

    for row in rows:
        print(row)

    cursor.close()
    conn.close()

if __name__ == '__main__':
    main()