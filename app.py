from bottle import error, default_app, get, run, static_file, view

############################################################
# INDEX
import routes.index

# 404
import routes.fourOhFour

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
