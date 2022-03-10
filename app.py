from bottle import error, default_app, get, run, view

############################################################
# INDEX
import routes.index

# 404
import routes.fourOhFour

############################################################
try:
    # Production
    import production

    application = default_app()
except:
    # Development
    run(host="127.0.0.1", port=3333, debug=True, reloader=True)
