import requests

def translate_text(text, source_lang='en', target_lang='hi'):
    url = "http://libretranslate:5000/translate"
    payload = {
        "q": text,
        "source": source_lang,
        "target": target_lang,
        "format": "text",
        "api_key": ""
    }
    response = requests.post(url, json=payload, timeout=10)
    if response.status_code == 200:
        print(f"Translation successful: {response.json()}")
        return response.json().get('translatedText') 
    else:
        return None
