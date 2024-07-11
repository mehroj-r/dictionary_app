from credentials import API_KEY  # Requires own API KEY to request API response
import requests


def request_word(word):
    request_session = requests.Session()

    URL = f"https://api.wordnik.com/v4/word.json/{word}/definitions"

    parameters = {
        "limit": "10",
        "includeRelated": "false",
        "sourceDictionaries": "wordnet",
        "useCanonical": "true",
        "includeTags": "false",
        "api_key": API_KEY,
    }

    response = request_session.get(url=URL, params=parameters)

    if response.status_code == 200:
        return extract_definitions(response.json())
    else:
        return False


def extract_definitions(response):
    definitions = {}
    for item in response:
        if 'partOfSpeech' not in item.keys():
            definitions['Error'] = ["The word is not in the dictionary."]
            return json_to_html(definitions)
        pfs = item['partOfSpeech']
        definition = item['text']
        if pfs not in definitions.keys():
            definitions[pfs] = []
        definitions[pfs].append(definition)
    return json_to_html(definitions)


def json_to_html(definitions):
    html_sample_light = ""
    html_sample_dark = ""
    count = 1

    list_pfs = list(definitions.keys())

    for pfs in list_pfs:
        html_sample_dark += f"<h5 style='color: #ffffff;'>{pfs.title()}</h5>"
        html_sample_light += f"<h5 style='color: #000000;'>{pfs.title()}</h5>"
        for definition in definitions[pfs]:
            html_sample_dark += f"<p style='color: #ffffff; font-size: 12px;'>‎ {count}. {definition}</p>"
            html_sample_light += f"<p style='color: #000000; font-size: 12px;'>‎ {count}. {definition}</p>"
            count += 1
        if list_pfs[-1] != pfs:
            html_sample_dark += "<div style='font-size: 1px;'>‎</div>"
            html_sample_light += "<div style='font-size: 1px;'>‎</div>"
        count = 1

    return html_sample_light, html_sample_dark
