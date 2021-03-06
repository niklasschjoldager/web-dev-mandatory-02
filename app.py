from bottle import error, default_app, get, run, static_file, view

# Routes
from routes import (
    all_tweets,
    bookmarks,
    fourOhFour,
    home,
    index,
    lists,
    logout,
    messages,
    notifications,
    search,
    user_profile,
)

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
from api.users import users_get, users_post

# Auth
import api.auth.login_post

############################################################
@get("/static/<file_path:path>")
def _(file_path):
    return static_file(file_path, root="./static")


############################################################
@get("/tweets/<file_path:path>")
def _(file_path):
    return static_file(file_path, root="./tweets")


############################################################
@get("/js/<file_name:path>")
def _(file_name):
    return static_file(file_name, root="./js")


############################################################
@get("/css/<file_name:path>")
def _(file_name):
    return static_file(file_name, root="./css")


############################################################
try:
    # Production
    import production

    application = default_app()
except:
    # Development
    run(host="127.0.0.1", port=3333, debug=True, reloader=True)
