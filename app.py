from bottle import error, default_app, get, run, static_file, view

############################################################
# ROUTES
from routes import fourOhFour, home, index

# API
import api.tweets.tweets_by_id_get
import api.tweets.tweets_delete
import api.tweets.tweets_get
import api.tweets.tweets_like_put
import api.tweets.tweets_post
import api.tweets.tweets_put
import api.tweets.tweets_unlike_put


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
