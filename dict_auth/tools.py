import random
import string



def generate_token():
    letters = string.ascii_letters

    shortened = letters[:30]

    stringed = "".join(shortened)

    return stringed



def api_key():
    return generate_token()+"dict-api"
