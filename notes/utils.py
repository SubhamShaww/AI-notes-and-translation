import requests

def translate_text(text, source_lang='en', target_lang='hi'):
    url = "https://libretranslate.de/translate"
    payload = {
        "q": text,
        "source": source_lang,
        "target": target_lang,
        "format": "text"
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        return response.json()['translatedText']
    else:
        return None
