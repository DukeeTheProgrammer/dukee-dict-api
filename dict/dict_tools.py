import requests


def get_word(word):
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        return data[0]
