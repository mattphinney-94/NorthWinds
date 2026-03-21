import pymysql
import cryptography

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

    cursor.execute('SELECT * FROM customers LIMIT 5')

    rows = cursor.fetchall()

    for row in rows:
        print(row)

    cursor.close()
    conn.close()

if __name__ == '__main__':
    main()