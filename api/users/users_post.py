from bottle import post, response, request

import jwt
import mysql.connector
import re
import time
import uuid

from g import (
    DATABASE_CONFIG,
    JSON_WEB_TOKEN_SECRET,
    REGEX_EMAIL,
    REGEX_PASSWORD,
    REGEX_USERNAME,
    USER_NAME_MAX_LENGTH,
    USER_NAME_MIN_LENGTH,
    USER_PASSWORD_MIN_LENGTH,
    USER_USERNAME_MAX_LENGTH,
    USER_USERNAME_MIN_LENGTH,
)

############################################################
@post("/users")
def _():
    try:
        ############################################################
        # Open Database
        database_connection = mysql.connector.connect(**DATABASE_CONFIG)
        database_cursor = database_connection.cursor()

        # Validate username
        if not request.forms.get("user_username"):
            response.status = 400
            return {"info": "Username is missing"}

        user_username = request.forms.get("user_username").strip().replace(" ", "")

        if len(user_username) < USER_USERNAME_MIN_LENGTH:
            response.status = 400
            return {"info": f"Username must be at least {USER_USERNAME_MIN_LENGTH} characters long"}

        if len(user_username) > USER_USERNAME_MAX_LENGTH:
            response.status = 400
            return {"info": f"Username can only have a maximum of {USER_USERNAME_MAX_LENGTH} characters"}

        if not re.match(REGEX_USERNAME, user_username):
            response.status = 400
            return {
                "info": "Username can only have letters from a-z (Uppercase and lowercase), numbers 0-9, underscores and hyphens"
            }

        query_username = f"""
            SELECT *
            FROM users
            WHERE user_username = %(user_username)s
        """

        database_cursor.execute(query_username, {"user_username": user_username})
        is_username_taken = database_cursor.fetchone()

        if is_username_taken:
            response.status = 400
            return {"info": "Username already exists - Forgot password?"}

        ############################################################
        # Validate email
        if not request.forms.get("user_email"):
            response.status = 400
            return {"info": "Email is missing"}

        user_email = request.forms.get("user_email").strip()

        if not re.match(REGEX_EMAIL, user_email):
            response.statis = 400
            return {"info": "Email is not invalid"}

        query_email = f"""
            SELECT *
            FROM users
            WHERE user_email = %(user_email)s
        """

        database_cursor.execute(query_email, {"user_email": user_email})
        is_email_registered = database_cursor.fetchone()

        if is_email_registered:
            response.status = 400
            return {"info": "Email already exists - Forgot your password?"}

        ############################################################
        # Validate password
        if not request.forms.get("user_password"):
            response.status = 400
            return {"info": "Password is missing"}

        user_password = request.forms.get("user_password")

        if len(user_password) < USER_PASSWORD_MIN_LENGTH:
            response.status = 400
            return {"info": f"Password must be at least {USER_PASSWORD_MIN_LENGTH} characters long"}

        if not re.match(REGEX_PASSWORD, user_password):
            response.status = 400
            return {
                "info": "Password must be at least 8 characters long, have 1 uppercase letter, 1 lowercase letter and 1 number or 1 symbol"
            }

        ############################################################
        # Validate name
        if not request.forms.get("user_name"):
            response.status = 400
            return {"info": "Name is missing"}

        user_name = request.forms.get("user_name").strip()

        if len(user_name) < USER_NAME_MIN_LENGTH:
            response.status = 400
            return {"info": f"Name must be at least {USER_NAME_MIN_LENGTH} characters long"}

        if len(user_name) > USER_NAME_MAX_LENGTH:
            response.status = 400
            return {"info": f"Name can only have a maximum of {USER_NAME_MAX_LENGTH} characters"}

        ############################################################

        # Create user
        user_created_at = int(time.time())
        user = (user_username, user_name, user_email, user_password, user_created_at)

        ############################################################
        # Add user
        query_add_user = f"""
            INSERT INTO users (user_id, user_username, user_name, user_email, user_password, user_created_at, user_updated_at, user_bio, user_is_active, user_website, user_location, user_birth_date, user_profile_image, user_cover_image)
            VALUES (NULL, %s, %s, %s, %s, %s, NULL, '', '1', '', '', NULL, '', '') 
        """

        database_cursor.execute(query_add_user, user)
        database_connection.commit()

        ############################################################

        add_user_session = f"""
            INSERT INTO user_sessions (user_session_id, user_session_iat) 
            VALUES (%s, %s)
        """

        # Create user session
        user_session_dict = {"user_session_id": str(uuid.uuid4()), "user_session_iat": int(time.time())}
        user_session_tuple = (user_session_dict["user_session_id"], user_session_dict["user_session_iat"])

        database_cursor.execute(add_user_session, user_session_tuple)
        database_connection.commit()

        ############################################################
        # Success

        encoded_jwt = jwt.encode(user_session_dict, JSON_WEB_TOKEN_SECRET, algorithm="HS256")
        response.set_cookie("user_session", encoded_jwt)
        response.status = 201
        return {"user_id": 12312312312}
    except Exception as ex:
        print(ex)
        response.status = 500
        return {"info": "Ups, something went wrong"}
    finally:
        if database_connection.is_connected():
            database_cursor.close()
            database_connection.close()
