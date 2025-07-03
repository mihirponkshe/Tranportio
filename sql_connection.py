import mysql.connector
import os

__cnx = None

def get_sql_connection_cursor():
    print("Opening MySQL connection...")
    global __cnx

    if __cnx is None:
        __cnx = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            port=int(os.getenv('DB_PORT', 3306)),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME')
        )

    return __cnx

