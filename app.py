from bottle import default_app, get, run, view

############################################################
# INDEX
import routes.index


############################################################
try:
    # Production
    import production

    application = default_app()
except:
    # Development
    run(host="127.0.0.1", port=3333, debug=True, reloader=True)
