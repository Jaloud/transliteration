import re
tests = [
    ["صَالِحٌ", "ṣāliḥun"],
    ["النَّار", "al-nār"],
    ["الحال", "al-ḥal"],
    ["ضِيَاء", "ḍiyāʾ"],
    ["المَرأَة", "al-marʾah"],
    ["يَس", "yāsīn"]
]

def transliterate(arabic_text):
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

    transliteration = ""

    prev_char = ""
    #مشكلة طه
    arabic_text = re.sub("ط?َه", "ṭāha", arabic_text)
    #مشكلة يس
    arabic_text = re.sub("(^|) يَس (.)", "yāsīn", arabic_text)

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


user_input = input('Enter text: ')
print(transliterate(user_input))


# print(transliterate("يَس"))
# print(transliterate("النَّار"))
# print(transliterate("الحال"))
# print(transliterate("ضِيَاء"))
# print(transliterate("المَرأَة"))

# for test in tests:
#         result = transliterate(test[0])
#         print(result, "/", test[1])
#         assert result == test[1]