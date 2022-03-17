from bottle import get, redirect, response, request, post

import jwt

from g import JSON_WEB_TOKEN_SECRET, user_sessions

############################################################
@post("/logout")
@get("/logout")
def _():
    try:
        if not request.get_cookie("user_session"):
            return redirect("/")

        encoded_user_session = request.get_cookie("user_session")
        jwt_decoded = jwt.decode(encoded_user_session, JSON_WEB_TOKEN_SECRET, algorithms=["HS256"])

        for index, session in enumerate(user_sessions):
            if jwt_decoded["session_id"] == session:
                user_sessions.pop(index)

        response.delete_cookie("user_session")
        return redirect("/")
    except jwt.exceptions.InvalidTokenError as ex:
        print(ex)
        response.delete_cookie("user_session")
        return redirect("/")
