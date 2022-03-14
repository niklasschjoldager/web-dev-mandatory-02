from bottle import get, view, redirect, response, request

import jwt

from g import JSON_WEB_TOKEN_SECRET, user_sessions

############################################################
@get("/")
@view("index")
def _():
    # Check if user already logged in via session
    if request.get_cookie("user_session"):
        print("Cookie exists!")
        try:
            encoded_user_session = request.get_cookie("user_session")
            jwt_decoded = jwt.decode(encoded_user_session, JSON_WEB_TOKEN_SECRET, algorithms=["HS256"])
            print("JWT decoded: ", jwt_decoded)

            for session in user_sessions:
                if jwt_decoded["session_id"] == session:
                    print("Session exists!")
                    return redirect("/home")
            response.delete_cookie("user_session")
        except jwt.exceptions.InvalidTokenError:
            response.delete_cookie("user_session")

    return
