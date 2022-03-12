# Temporary
users = [
    {
        "user_id": "5f5f311d-ca9b-481b-8846-f7db449270f8",
        "user_username": "niklasschjoldager",
        "user_name": "Niklas Schjoldager",
        "user_email": "test@mail.dk",
        "user_password": "1234",
    }
]
user_sessions = []
tweets = []


###########################################################
USER_NAME_MIN_LENGTH = 2
USER_NAME_MAX_LENGTH = 50
USER_USERNAME_MAX_LENGTH = 20
USER_PASSWORD_MIN_LENGTH = 8
USER_USERNAME_MIN_LENGTH = 4


###########################################################
REGEX_EMAIL = '^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$'
REGEX_PASSWORD = "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$ %^&*-]).{8,}$"
REGEX_UUID4 = "^[0-9a-f]{8}\b-[0-9a-f]{4}\b-[0-9a-f]{4}\b-[0-9a-f]{4}\b-[0-9a-f]{12}$"
REGEX_USERNAME = "^[a-zA-Z0-9_-]{4,20}$"
