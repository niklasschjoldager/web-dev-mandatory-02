from bottle import redirect, response, request, post

import jwt
import mysql.connector
import re
import time
import uuid

from g import DATABASE_CONFIG, JSON_WEB_TOKEN_SECRET, REGEX_EMAIL, REGEX_PASSWORD, users, user_sessions
from utils.user_session import validate_user_session

############################################################
@post("/login")
def _():
    validate_user_session("/home")

    # Validate email
    if not request.forms.get("user_email"):
        response.status = 400
        return {"info": "Missing email"}

    user_email = request.forms.get("user_email").strip()

    if not re.match(REGEX_EMAIL, user_email):
        response.statis = 400
        return {"info": "Email is not invalid"}

    # Validate Password
    if not request.forms.get("user_password"):
        response.status = 400
        return {"info": "Missing password"}

    user_password = request.forms.get("user_password")

    if not re.match(REGEX_PASSWORD, user_password):
        response.status = 400
        return {"info": "Invalid password"}

    # Validate email & password with users in database
    connection = mysql.connector.connect(**DATABASE_CONFIG)
    cursor = connection.cursor(dictionary=True)

    query_login = f"""
        SELECT *
        FROM users
        WHERE user_email = %(user_email)s
    """

    cursor.execute(query_login, {"user_email": user_email})
    user_in_database = cursor.fetchone()

    if not user_in_database:
        response.status = 400
        return {"info": "E-mail does not exist"}

    if user_in_database["user_password"] != user_password:
        response.status = 400
        return {"info": "Wrong password"}

    # Create user session
    user_session_dict = {"user_session_id": str(uuid.uuid4()), "user_session_iat": int(time.time())}
    user_session_tuple = (user_session_dict["user_session_id"], user_session_dict["user_session_iat"])

    # Add user session
    query_add_user_session = f"""
        INSERT INTO user_sessions (user_session_id, user_session_iat) 
        VALUES (%s, %s)
    """
    cursor.execute(query_add_user_session, user_session_tuple)
    connection.commit()

    encoded_jwt = jwt.encode(user_session_dict, JSON_WEB_TOKEN_SECRET, algorithm="HS256")
    response.set_cookie("user_session", encoded_jwt)

    return redirect("/home")
