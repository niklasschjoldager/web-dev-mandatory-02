from bottle import error, default_app, get, run, static_file, view

# Routes
from routes import fourOhFour, home, index

# Tweets
from api.tweets import (
    tweets_by_id_get,
    tweets_delete,
    tweets_get,
    tweets_like_put,
    tweets_post,
    tweets_put,
    tweets_unlike_put,
)

# Users
import api.users.users_get
import api.users.users_post


############################################################
@get("/static/<file_path:path>")
def _(file_path):
    return static_file(file_path, root="./static")


############################################################
try:
    # Production
    import production

    application = default_app()
except:
    # Development
    run(host="127.0.0.1", port=3333, debug=True, reloader=True)
