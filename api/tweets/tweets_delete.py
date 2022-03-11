from bottle import delete

############################################################
@delete("/tweets/<tweet_id>")
def _(tweet_id):
    # Validate
    # Connect to the db
    # Delete the tweet
    # If tweet deleted, send a status of 200
    # If tweet not found, send a 400 (Correct one: 204)
    return tweet_id
