from bottle import redirect, response, request, post

from g import user_sessions

############################################################
@post("/logout")
def _():
    if not request.get_cookie("user_session"):
        redirect("/")

    user_session = request.get_cookie("user_session")

    if user_session in user_sessions:
        user_sessions.remove(user_session)

    response.delete_cookie("user_session")

    return redirect("/")
