from bottle import put, request, response
import imghdr
import mysql.connector
import os
import uuid

from utils.user_session import validate_user_session
from g import (
    DATABASE_CONFIG,
    TWEET_IMAGE_ALLOWED_FILE_EXTENSIONS,
    TWEET_IMAGE_PATH,
    TWEET_TEXT_MAX_LENGTH,
    TWEET_TEXT_MIN_LENGTH,
)

###########################################################
@put("/tweets/<tweet_id>")
def _(tweet_id):
    validate_user_session()

    try:
        # Validate tweet ID
        if not tweet_id:
            response.status = 400
            return {"info": "Tweet ID is missing"}

        tweet_id = int(tweet_id)

        if tweet_id < 1:
            response.status = 400
            return {"info": "Tweet ID is not a valid ID"}

        query_set_parts = []
        query_params = {"tweet_id": tweet_id}

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

        query_set_parts.append("tweet_text = %(tweet_text)s")
        query_params["tweet_text"] = tweet_text

        ############################################################
        # Validate media (image / video)
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

            query_set_parts.append("tweet_image_file_name = %(tweet_image)s")
            query_params["tweet_image"] = image_name

        query_set_parts = ",".join(query_set_parts)

        # ############################################################
        # # Connect to the db
        connection = mysql.connector.connect(**DATABASE_CONFIG)
        cursor = connection.cursor()

        query_edit_tweet = f"""
            UPDATE tweets 
            SET {query_set_parts}
            WHERE tweet_id = %(tweet_id)s
        """

        cursor.execute(query_edit_tweet, query_params)
        connection.commit()
        print(query_set_parts)
        print(query_params)

        # Success
        response.status = 200
        return "Success"
    except Exception as ex:
        print(ex)
        response.status = 500
        return {"info": "Ups, something went wrong"}
