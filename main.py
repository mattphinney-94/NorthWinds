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

    cursor.execute('SELECT * FROM customers LIMIT 5')

    rows = cursor.fetchall()

    for row in rows:
        print(row)

    cursor.close()
    conn.close()

if __name__ == '__main__':
    main()