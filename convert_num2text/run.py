import re
from convert_num2text.convertor import num2word, num_en2km


def textNorm(text):
    text = re.sub(r"[0-9]+", num_en2km, text)
    text = re.sub(r"[+-]?([០-៩]*[,])?[០-៩]+", num2word, text)
    curlist = {
        "$": "ដុល្លារ",
        "៛": "រៀល",
        "€": "អឺរ៉ូ",
        "¥": "យេន",
        "￥": "យន់",
        "₹": "រូពី",
        "£": "ផោន",
        "฿": "បាត",
        "₫": "ដុង",
        "₭": "គីប",
    }
    punctuation = r"!?,.;។"
    if (text[-1] != punctuation) : text = text + ';'
    text = re.sub(r"[$៛€¥￥₹£฿₫₭]", lambda m: curlist.get(m.group()), text)
    print(text)
    return text

