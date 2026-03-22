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

    cursor.execute('SELECT * FROM customers LIMIT 5')

    rows = cursor.fetchall()

    for row in rows:
        print(row)

    cursor.close()
    conn.close()

if __name__ == '__main__':
    main()