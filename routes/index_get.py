from bottle import get, view

############################################################
import sqlite3
import uuid

############################################################
@get("/")
@view("index")
def _():
    return
