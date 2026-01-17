import requests


def get_word(word):
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        return {
                "word":word,
                "meaning":f"{data[0]["meanings"][0]["definitions"][0]["definition"]}",
                "transcription": data[0]['phonetics'][0]["text"],
                "partOfSpeech":f"{data[0]["meanings"][0]["partOfSpeech"]}",
                "audio":data[0]["phonetics"][0]["audio"],
                "copywright":"2026 Dukee-Dict-API All rights reserved."
                }
