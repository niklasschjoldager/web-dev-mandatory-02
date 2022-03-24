from bottle import get, view, redirect, response, request, template

import jwt
import mysql.connector
from utils.user_session import validate_user_session

from g import DATABASE_CONFIG, JSON_WEB_TOKEN_SECRET

############################################################
@get("/home")
def _():
    validate_user_session(None, "/")

    try:
        connection = mysql.connector.connect(**DATABASE_CONFIG)
        cursor = connection.cursor(dictionary=True)

        query_get_user_tweets = f"""
            SELECT *
            FROM users, tweets
            WHERE tweets.tweet_fk_user_id = users.user_id
            ORDER BY tweet_created_at DESC
        """
        cursor.execute(query_get_user_tweets)
        tweets = cursor.fetchall()

        return template("home", dict(tweets=tweets))
    except Exception as ex:
        print(ex)
        response.status = 500
        return {"info": "Ups, something went wrong"}
