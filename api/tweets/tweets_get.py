from bottle import get

###########################################################
@get("/tweets")
def _():
    # Validate
    # Who likes it? The user who is logged in
    # Connect to the db
    # Update / insert the liked tweet
    return "Tweets received"
