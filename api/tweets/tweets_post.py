from bottle import post, redirect, response, request

import jwt
import uuid

from g import JSON_WEB_TOKEN_SECRET, tweets, TWEET_TEXT_MAX_LENGTH, TWEET_TEXT_MIN_LENGTH, user_sessions

############################################################
@post("/tweets")
def _():
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
    # Create tweet
    tweet_id = str(uuid.uuid4())
    tweet = {"tweet_id": tweet_id, "tweet_text": tweet_text}

    ############################################################
    # Add tweet
    tweets.append(tweet)

    ############################################################
    # Connect to the db
    # Insert the tweet in the tweets table

    print(jwt_decoded)

    # Success
    response.status = 201
    return tweet
