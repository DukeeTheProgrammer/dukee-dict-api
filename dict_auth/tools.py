import random
import string



def generate_token():
    letters = string.ascii_letters

    shortened = [random.choice(letters) for _ in range(30)]

    stringed = "".join(shortened)

    return stringed



def api_key():
    return "dd_api_"+generate_token()
