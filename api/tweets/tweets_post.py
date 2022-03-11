from bottle import post, response, request
import uuid

############################################################
@post("/tweets")
def _():
    # Validate (min max)
    # Validate user credentials
    # Connect to the db
    # Insert the tweet in the tweets table
    response.status = 201
    tweet_text = request.forms.get("tweet_text")
    tweet_id = str(uuid.uuid4())
    tweet = {"tweet_id": tweet_id, "tweet_text": tweet_text}

    return tweet
