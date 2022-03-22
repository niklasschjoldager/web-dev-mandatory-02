from bottle import get, view, redirect, response, request

import jwt
import mysql.connector
from utils.user_session import validate_user_session

from g import DATABASE_CONFIG, JSON_WEB_TOKEN_SECRET

############################################################
@get("/home")
@view("home")
def _():
    validate_user_session(None, "/")
