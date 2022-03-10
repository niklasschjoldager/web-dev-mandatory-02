from bottle import get, view

############################################################
@get("/home")
@view("home")
def _():
    return
