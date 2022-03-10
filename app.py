from bottle import error, default_app, get, run, static_file, view

############################################################
# GET
import routes.index_get
import routes.home_get
import routes.fourOhFour_get


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
