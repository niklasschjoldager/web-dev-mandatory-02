import mysql.connector
from mysql.connector import errorcode

config = {"user": "root", "password": "root", "host": "127.0.0.1", "port": 8889, "database": "tweeter_exercise"}

try:
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()

    query = f"""
        SELECT *
        FROM users
    """

    cursor.execute(query)

    for user in cursor:
        print(user)
except mysql.connector.Error as error:
    print(error)
finally:
    connection.close()
