from bottle import get, view, redirect, response, request

import jwt

from g import JSON_WEB_TOKEN_SECRET, user_sessions

############################################################
@get("/home")
@view("home")
def _():

    if not request.get_cookie("user_session"):
        return redirect("/")

    try:
        encoded_user_session = request.get_cookie("user_session")
        jwt_decoded = jwt.decode(encoded_user_session, JSON_WEB_TOKEN_SECRET, algorithms=["HS256"])

        for session in user_sessions:
            if jwt_decoded["session_id"] == session:
                return

        response.delete_cookie("user_session")
        return redirect("/")
    except jwt.exceptions.InvalidTokenError:
        response.delete_cookie("user_session")
        return redirect("/")
