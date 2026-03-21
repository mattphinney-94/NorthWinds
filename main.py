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

    while selection != 7:
        print('1. Add customer')
        print('2. Add order')
        print('3. Remove order')
        print('4. Ship order')
        print('5. Print pending orders')
        print('6. More options')
        print('7. Exit')

    cursor.execute('SELECT * FROM customers LIMIT 5')

    rows = cursor.fetchall()

    for row in rows:
        print(row)

    cursor.close()
    conn.close()