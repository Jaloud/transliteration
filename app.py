from flask import Flask, request, render_template
import re
import asyncio
from pybelqis import Belqis
import os

b = Belqis(token=os.environ.get('BELQIS_TOKEN'))
b = Belqis(token='eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6IkFiZHVsbGFoQWxtYW5laSIsImV4cCI6MTY3ODIzNzQ2Miwib3JpZ0lhdCI6MTY3ODIzNzE2Mn0.Ot-zD6exsbJR2AtRGGrINjbtDsPhmJNUUXVzFVxQDLo')


rules = {
    "ء": "ʾ",
    "آ": "ā",
    "أ": "a",
    "ؤ": "ʾ",
    "ئ": "ʾ",
    "إ": "i",
    "أُ": "u",
    "ا": "a",
    "اِ": "i",
    "ب": "b",
    "ة": "h",
    "ت": "t",
    "ث": "th",
    "ج": "j",
    "ح": "ḥ",
    "خ": "kh",
    "د": "d",
    "ذ": "dh",
    "ر": "r",
    "ز": "z",
    "س": "s",
    "ش": "sh",
    "ص": "ṣ",
    "ض": "ḍ",
    "ط": "ṭ",
    "ظ": "ẓ",
    "ع": "ʿ",
    "غ": "gh",
    "ف": "f",
    "ق": "q",
    "ك": "k",
    "ل": "l",
    "م": "m",
    "ن": "n",
    "ه": "h",
    "و": "w",
    "ى": "a",
    "ي": "y",
    "َ": "a",
    "ُ": "u",
    "ِ": "i",
    "ً": "an",
    "ٌ": "un",
    "ٍ": "in",
    "َ" + "ا": "ā",
    "َ" + "ى": "ā",
    "ُ" + "و": "ū",
    "ِ" + "ي": "ī",
    "ِ" + "يَ": "iy",
    "ةَ": "ta",
    "ةِ": "ti",
    "ةُ": "tu",
    "ةً": "tan",
    "ةٍ": "tin",
    "ةٌ": "tun",
    "وا": "ū",
    "أَ": "ʾa",
    "أْ": "ʾ",
}

def transliterate(arabic_text):
    transliteration = ""

    prev_char = ""
    #مشكلة طه
    arabic_text = re.sub("ط?َه", "ṭāha", arabic_text)
    #مشكلة يس
    arabic_text = re.sub("( |^)يَس( |$)", "yāsīn", arabic_text)

    arabic_text = re.sub("الله", "allah", arabic_text)

    arabic_text = re.sub("الرَّحمَ?ن", "al-raḥmān", arabic_text)

    # sunny AL الشمسية
    arabic_text = re.sub("(^| )ال(.)ّ", "\g<1>al-\g<2>", arabic_text)

    # moony AL القمرية
    arabic_text = re.sub("(^| )ال", "\g<1>al-", arabic_text)
    # مشكلة أحمد
    arabic_text = re.sub("(^| )أَ", "\g<1>a", arabic_text)

    # yaa مشكلة ضياء
    arabic_text = re.sub("يَاء", "yāʾ", arabic_text)
    # مشكلة مواساة
    arabic_text = re.sub("وَا", "wā", arabic_text)
    # مشكلة ابن تيمية
    arabic_text = re.sub("يَّ", "yya", arabic_text)
    # مشكلة واعتصموا

    #مشكلة بالله

    for i, char in enumerate(arabic_text):
        if prev_char + char in rules:
            transliteration = transliteration[:-1]
            transliteration += rules[prev_char + char]
            prev_char = char
        elif char in rules:
            transliteration += rules[char]
            prev_char = char
        elif char == "\u0651":
            transliteration += rules[prev_char]
        else:
            transliteration += char
            prev_char = char
    return transliteration

async def tash(belqis_client, arabic_text):
    # This function takes two arguments:
    # belqis_client: a Belqis object that has an authentication token
    # arabic_text: a string of Arabic text to be diacritized and transliterated

    # It retrieves the diacritized version of the input arabic_text using the tashkeel method from the Belqis API, and then returns its transliterated version using the transliterate function.

    # Returns:
    # str: The transliterated version of the diacritized arabic_text.

    r = await belqis_client.tashkeel(arabic_text)
    return transliterate(next(iter(r.values())))


from flask import Flask, request

app = Flask(__name__, static_folder='static')

@app.route('/')
def index():
    return render_template('index.html')
  
@app.route("/process", methods=["POST"])
def process():
    user_input = request.form["user_input"]
    result = transliterate(user_input)
    return result

@app.route("/process_diacritics", methods=["POST"])
def process_diacritics():
    user_input = request.form["user_input"]
    added_diacritics = asyncio.run(tash(b, user_input))
    transliterated_dict= transliterate(added_diacritics)
    return transliterated_dict


if __name__ == '__main__':
    app.run(debug=True)
