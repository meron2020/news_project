import requests
import string

string_letters = string.ascii_letters
string_upper = string.ascii_uppercase


class HebrewMorphologyEngine:
    def __init__(self):
        self.ip = "http://34.65.165.8:8000/yap/heb/joint"

    def request_json(self, text):
        data = '{"text": "' + text + '  "}'
        response = requests.get(self.ip,
                                data=data.encode(
                                    "utf-8"),
                                headers={
                                    "Content-Type": "application/json"
                                },
                                cookies={},
                                auth=(),
                                )

        split_response = response.json()['md_lattice'].split()
        new_response_list = []
        for string in split_response:
            try:
                int(string)
            except Exception:
                new_response_list.append(string)
        return new_response_list

    @classmethod
    def return_hebrew_words_list(cls, new_response_list):
        hebrew_words = []
        for word in new_response_list:
            if word[0] in string_letters:
                pass
            else:
                hebrew_words.append(word)

        return hebrew_words

    @classmethod
    def base_words(cls, hebrew_words_list):
        full_hebrew_words = []
        for hebrew_word in hebrew_words_list:
            if len(hebrew_word) != 1:
                full_hebrew_words.append(hebrew_word)

        base_words = {}
        for i in range(len(full_hebrew_words)):
            if i % 2 == 0:
                base_words[full_hebrew_words[i]] = full_hebrew_words[i + 1]
        return base_words

    @classmethod
    def morph_engine_base_words(cls, text):
        morph_engine = HebrewMorphologyEngine()
        response_list = morph_engine.request_json(text)
        hebrew_words_list = HebrewMorphologyEngine.return_hebrew_words_list(response_list)
        base_words = HebrewMorphologyEngine.base_words(hebrew_words_list)
        return base_words
