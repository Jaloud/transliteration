from flask import Flask, request, render_template
import re
import os
from camel_tools.utils.normalize import normalize_unicode
from camel_tools.utils.dediac import dediac_ar
from camel_tools.tokenizers.word import simple_word_tokenize
from camel_tools.disambig.mle import MLEDisambiguator
from camel_tools.tokenizers.morphological import MorphologicalTokenizer
from camel_tools.utils.charmap import CharMapper






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

def transliterate(tokens):
    arabic_text = ''.join(tokens)
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
    # user_input_normalized = normalize_unicode(user_input)
    # user_input_dediac = dediac_ar(user_input_normalized)
    # We can output diacritized tokens by setting `diac=True
    mle = MLEDisambiguator.pretrained('calima-msa-r13')
    tokenizer = MorphologicalTokenizer(mle, scheme='d3tok', split=True, diac=True)
    tokens = tokenizer.tokenize(user_input)
    print(tokens)
    arabic_text = ''.join(tokens)
    return arabic_text

if __name__ == '__main__':
    app.run(debug=True)