from bottle import redirect, response, request, post

import jwt
import re
import time
import uuid

from g import JSON_WEB_TOKEN_SECRET, REGEX_EMAIL, REGEX_PASSWORD, users, user_sessions

############################################################
@post("/login")
def _():
    # Check if user already logged in via session
    if request.get_cookie("user_session"):
        try:
            encoded_user_session = request.get_cookie("user_session")
            jwt_decoded = jwt.decode(encoded_user_session, JSON_WEB_TOKEN_SECRET, algorithms=["HS256"])

            for session in user_sessions:
                if jwt_decoded["session_id"] == session:
                    return redirect("/home")
            response.delete_cookie("user_session")
        except jwt.exceptions.InvalidTokenError as ex:
            print(ex)
            response.delete_cookie("user_session")

    # Validate email
    if not request.forms.get("user_email"):
        response.status = 400
        return {"info": "Missing email"}

    user_email = request.forms.get("user_email").strip()

    if not re.match(REGEX_EMAIL, user_email):
        response.statis = 400
        return {"info": "Email is not invalid"}

    user_index = None

    for index, user in enumerate(users):
        if user["user_email"] == user_email:
            user_index = index
            break
        response.status = 400
        return {"info": "E-mail does not exist"}

    # Validate Password
    if not request.forms.get("user_password"):
        response.status = 400
        return {"info": "Missing password"}

    user_password = request.forms.get("user_password")

    if not re.match(REGEX_PASSWORD, user_password):
        response.status = 400
        return {"info": "Invalid password"}

    if not users[user_index]["user_password"] == user_password:
        response.status = 400
        return {"info": "Wrong password"}

    # Create user session
    user_session_id = str(uuid.uuid4())
    user_session = {"session_id": user_session_id, "iat": int(time.time())}
    user_sessions.append(user_session_id)

    # Success
    encoded_jwt = jwt.encode(user_session, JSON_WEB_TOKEN_SECRET, algorithm="HS256")
    response.set_cookie("user_session", encoded_jwt)
    return redirect("/home")
