from bottle import post, response

############################################################
@post("/users")
def _():
    return "User created"
