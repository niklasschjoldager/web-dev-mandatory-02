import mysql.connector

config = {"user": "root", "password": "root", "host": "127.0.0.1", "port": 8889, "database": "tweeter_exercise"}

try:
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()

    add_user = f"""
      INSERT INTO users (user_id, user_username, user_first_name, user_last_name, user_email, user_password, user_created_at, user_updated_at, user_bio, user_is_active, user_website, user_location, user_birth_date, user_profile_image, user_cover_image)
      VALUES (NULL, 'niklasschjoldager', 'Niklas', 'Schjoldager', 'minsejemail@mail.dk', 'MyCoolPassword123!', '123123123', NULL, '', '1', '', '', NULL, '', '') 
    """

    cursor.execute(add_user)
    connection.commit()
    print(cursor.rowcount, "Record inserted successfully into Users table")
except mysql.connector.Error as error:
    print(error)
finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
