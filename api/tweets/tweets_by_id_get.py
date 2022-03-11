from bottle import get

###########################################################
@get("/tweets/<tweet_id>")
def _(tweet_id):
    # Validate
    # Who likes it? The user who is logged in
    # Connect to the db
    # Update / insert the liked tweet
    return "Tweet received"
