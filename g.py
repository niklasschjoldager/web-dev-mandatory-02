# Temporary
users = [
    {
        "user_id": "5f5f311d-ca9b-481b-8846-f7db449270f8",
        "user_username": "niklasschjoldager",
        "user_name": "Niklas Schjoldager",
        "user_email": "test@mail.dk",
        "user_password": "Mypassword123!",
    },
    {
        "user_id": "5739a9aa-1d86-4604-8471-aca0e710d007",
        "user_username": "HansHansen",
        "user_name": "Hans hansen",
        "user_email": "hans@hansen.dk",
        "user_password": "Mypassword123!",
    },
]

user_sessions = []
tweets = []


###########################################################
JSON_WEB_TOKEN_SECRET = "699js!ihTri94t@sa129d90waj0cjh428h824h5298h"

###########################################################
TWEET_TEXT_MIN_LENGTH = 1
TWEET_TEXT_MAX_LENGTH = 255

USER_NAME_MAX_LENGTH = 50
USER_NAME_MIN_LENGTH = 2
USER_USERNAME_MAX_LENGTH = 20
USER_USERNAME_MIN_LENGTH = 4
USER_PASSWORD_MIN_LENGTH = 8

###########################################################
REGEX_EMAIL = '^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$'
REGEX_PASSWORD = "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$ %^&*-]).{8,}$"
REGEX_USERNAME = "^[a-zA-Z0-9_-]{4,20}$"
REGEX_UUID4 = "^[0-9a-f]{8}\b-[0-9a-f]{4}\b-[0-9a-f]{4}\b-[0-9a-f]{4}\b-[0-9a-f]{12}$"
