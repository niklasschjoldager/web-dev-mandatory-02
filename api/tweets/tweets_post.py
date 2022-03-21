from bottle import post, redirect, response, request

import imghdr
import jwt
import os
import uuid

from g import (
    JSON_WEB_TOKEN_SECRET,
    TWEET_IMAGE_ALLOWED_FILE_EXTENSIONS,
    TWEET_IMAGE_PATH,
    TWEET_TEXT_MAX_LENGTH,
    TWEET_TEXT_MIN_LENGTH,
    user_sessions,
)

############################################################
@post("/tweets")
def _():
    ############################################################
    # Validate if user is logged in
    if not request.get_cookie("user_session"):
        return redirect("/")

    try:
        is_user_logged_in = False
        encoded_user_session = request.get_cookie("user_session")
        jwt_decoded = jwt.decode(encoded_user_session, JSON_WEB_TOKEN_SECRET, algorithms=["HS256"])

        for session in user_sessions:
            if jwt_decoded["session_id"] == session:
                is_user_logged_in = True

        if not is_user_logged_in:
            response.delete_cookie("user_session")
            return redirect("/")

    except jwt.exceptions.InvalidTokenError as ex:
        print(ex)
        response.delete_cookie("user_session")
        return redirect("/")

    ############################################################
    # Validate text
    if not request.forms.get("tweet_text"):
        response.status = 400
        return {"info": "Tweet text is missing"}

    tweet_text = request.forms.get("tweet_text").strip()

    if len(tweet_text) < TWEET_TEXT_MIN_LENGTH:
        response.status = 400
        return {"info": f"Tweet must be at least {TWEET_TEXT_MIN_LENGTH} characters long"}

    if len(tweet_text) > TWEET_TEXT_MAX_LENGTH:
        response.status = 400
        return {"info": f"Tweet can only have a maximum of {TWEET_TEXT_MAX_LENGTH} characters"}

    ############################################################
    # Validate media (image / video)
    image_url = None

    if request.files.get("tweet_image"):
        image = request.files.get("tweet_image")
        file_name, file_extension = os.path.splitext(image.filename)

        if file_extension not in TWEET_IMAGE_ALLOWED_FILE_EXTENSIONS:
            response.status = 400
            return {"info": f"Image format not allowed"}

        # Convert old .jpg extension to .jpeg, so it passes imghdr.what validation
        if file_extension == ".jpg":
            file_extension = ".jpeg"

        image_id = str(uuid.uuid4())
        image_name = f"{image_id}{file_extension}"
        image_path = f"{TWEET_IMAGE_PATH}/{image_name}"

        image.save(image_path)
        validated_file_extension = imghdr.what(image_path)

        if file_extension != f".{validated_file_extension}":
            os.remove(image_path)
            response.status = 400
            return {"info": "Invalid image format"}

        image_url = image_path

    ############################################################
    # Create tweet
    tweet_id = str(uuid.uuid4())
    tweet = {"id": tweet_id, "text": tweet_text, "imageUrl": image_url}

    ############################################################
    # Connect to the db
    # Insert the tweet in the tweets table

    # Success
    response.status = 201
    return tweet
