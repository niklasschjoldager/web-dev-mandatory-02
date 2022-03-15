from bottle import post, response, request

import re
import time
import uuid

from g import (
    REGEX_EMAIL,
    REGEX_PASSWORD,
    REGEX_USERNAME,
    users,
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

        for user in users:
            if user["user_username"] == user_username:
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

        for user in users:
            if user["user_email"] == user_email:
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
        user_id = str(uuid.uuid4())
        user_created_at = int(time.time())
        user = {
            "user_id": user_id,
            "user_created_at": user_created_at,
            "user_email": user_email,
            "user_name": user_name,
            "user_password": user_password,
            "user_username": user_username,
        }

        # TODO: Add user session

        ############################################################
        # Add user
        users.append(user)

        ############################################################
        # Success
        response.status = 201
        return {"user_id": user_id}
    except Exception as ex:
        print(ex)
        response.status = 500
        return {"info": "Ups, something went wrong"}
