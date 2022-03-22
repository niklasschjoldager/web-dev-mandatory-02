from bottle import get, view, redirect, response, request

import jwt
import mysql.connector

from g import DATABASE_CONFIG, JSON_WEB_TOKEN_SECRET

############################################################
@get("/home")
@view("home")
def _():
    # Validate if user is logged in
    if not request.get_cookie("user_session"):
        return redirect("/")

    try:
        encoded_user_session = request.get_cookie("user_session")
        jwt_decoded = jwt.decode(encoded_user_session, JSON_WEB_TOKEN_SECRET, algorithms=["HS256"])

        connection = mysql.connector.connect(**DATABASE_CONFIG)
        cursor = connection.cursor(dictionary=True)

        query_user_session = f"""
            SELECT *
            FROM user_sessions
            WHERE user_session_id = %(user_session_id)s
        """

        cursor.execute(query_user_session, {"user_session_id": jwt_decoded["user_session_id"]})
        is_user_session_valid = cursor.fetchone()

        if is_user_session_valid and is_user_session_valid["user_session_id"] == jwt_decoded["user_session_id"]:
            return

        response.delete_cookie("user_session")
        return redirect("/")
    except jwt.exceptions.InvalidTokenError as ex:
        print(ex)
        response.delete_cookie("user_session")
        return redirect("/")
