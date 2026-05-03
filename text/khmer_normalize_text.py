
# ---------------------------------------------------------------------------- #
# |                            mixed english & khmer tokenizer               | #
# ---------------------------------------------------------------------------- #
# ---------------------------------------english------------------------------------- #
# check if it is a english word
import re
from num2words import num2words
import nltk
from nltk.util import ngrams
from nltk.tokenize import word_tokenize

# Download required NLTK resources
# nltk.download('all')
# nltk.download('punkt')

# Function to check if a word contains only English characters
def is_english(word):
    return bool(re.match(r'^[a-zA-Z0-9\'\-]+$', word))  # Allows letters, numbers, apostrophes, and hyphens

def eng_normalization(text, n=1):

    # Separate letters from numbers (e.g., "abc123" -> "abc 123")
    text = re.sub(r'([a-zA-Z])(\d)', r'\1 \2', text)
    text = re.sub(r'(\d)([a-zA-Z])', r'\1 \2', text)

    # Tokenize the text
    tokens = word_tokenize(text)

    # Convert numbers to words
    # tokens = [num2words(token) if token.isdigit() else token for token in tokens]
    return " ".join(tokens)  # Return a string instead of a list


# ---------------------------------------Khmer------------------------------------- #

from khmernltk import word_tokenize as khmer_tokenize
import re
from khmerspell import khnormal
from convert_num2text import *
# from text.cleaners import fix_virama, replace_percentage



def khmer_normalization(text):
    original_text = text

    # Step 1: normalize and clean
    text = khnormal(text)
    text = re.sub(r'\s+', '', text).strip()
    text = text.replace('\u200b','').replace('\ufeff', '')
    text = re.sub(r'[\u200b\ufeff]', '', text)

    # Step 2: Convert numbers before tokenization
    def convert_match(match):
        number_string = match.group(0)
        try:
            if number_string.count(',') >= 2 and '.' not in number_string:
                return convert_number_to_words(number_string)
            elif ',' in number_string and '.' in number_string:
                return convert_khmer_float_to_words(number_string)
        except Exception as e:
            print(f"Number conversion error: {e}")
        return number_string

    text = re.sub(r'\d[\d,\.]*', convert_match, text)

    # Step 3: Tokenization
    tokens = khmer_tokenize(text)
    tokens = ' '.join(tokens)

    # Step 4: Clean symbols
    tokens = re.sub(r'\s+', ' ', tokens).strip()
    tokens = re.sub(r'[\^\*\+\?\{\}\[\]\\\|\(\)"]',' ',tokens)
    tokens = re.sub(r'[«»៕។▁]', ' ', tokens)

    # Step 5: Final conversions
    for func in [
        convert_khmer_date_to_words,
        convert_khmer_time_to_words,
        convert_khmer_telephone_to_words,
        convert_khmer_float_to_words,
        convert_number_to_words,
        textNorm
    ]:
        try:
            return func(tokens)
        except:
            pass

    return tokens


# ---------------------------------------------------------------------------- #
# |                               Khmer abbreviation                         | #
# ---------------------------------------------------------------------------- #
import re
from text.abbreviation import khmer_abbreviation

def replace_percentage(text, mapping=khmer_abbreviation):
    """Replace characters in text based on the mapping dictionary."""
    for key, value in mapping.items():
        text = re.sub(r'(\d+)\s*' + re.escape(key), r'\1' + value, text)  # Replace numbers followed by %
        text = re.sub(r'[\^\\*\+\?\{\}\[\]\\\|\(\)"]','',text)
        text = re.sub(r'▁','',text)
        text = re.sub(r':','',text)
        text = text.replace(key, value)  # Replace standalone %
    return text


# fix virama in khmer text "ឆ្នាំ្"to "​ឆ្នាំ"
def fix_virama(text):
    text = re.sub(r'\u17D2+$', '', text)
    text = re.sub(r'\u17D2(?![\u1780-\u17A2])', '', text)
    return text





# def replace_percentage(text, mapping=khmer_abbreviation):
#     for key, value in mapping.items():
#         # Replace number + unit pattern (e.g., "10 %", "100 ស.វ")
#         text = re.sub(r'(\d+)\s*' + re.escape(key), r'\1' + value, text)
        
#         # Replace stand-alone abbreviations (not after numbers)
#         text = re.sub(r'\b' + re.escape(key) + r'\b', value, text)
#     return text

# def replace_percentage(text, mapping=khmer_abbreviation):
#     for key, value in mapping.items():
#         # Case 1: Replace number + unit (e.g. 10 %, ៥ ស.វ)
#         pattern_with_number = r'(\d+)\s*' + re.escape(key)
#         text = re.sub(pattern_with_number, r'\1' + value, text)

#         # Case 2: Replace abbreviation at the beginning of a compound (e.g., ស.វទី៥)
#         pattern_prefix = re.escape(key) + r'(?=\w)'
#         text = re.sub(pattern_prefix, value, text)

#         # Case 3: Replace standalone key
#         text = text.replace(key, value)
#     return text


# def kh_tokenize_text(text: str, vocab, *args, **kwargs):
#     # Normalize abbreviations and symbols first (applies to both scripts)
#     text = replace_percentage(text)
#     text = fix_virama(text)

#     # Separate mixed text
#     eng_part = []
#     khmer_part = []

#     # Split the text into chunks: Khmer or English tokens
#     for word in re.findall(r'\w+|\W+', text):
#         if is_english(word):
#             eng_part.append(word)
#         else:
#             khmer_part.append(word)

#     # Normalize both parts
#     eng_text = eng_normalization(" ".join(eng_part)) if eng_part else ""
#     khmer_text = khmer_normalization("".join(khmer_part)) if khmer_part else ""

#     # Merge and tokenize
#     final_text = (eng_text + " " + khmer_text).strip()
#     tokens = final_text.split()

#     # Convert to token indices
#     return vocab(tokens)


# ---------------------------------------------------------------------------- #
# |                               New Khmer tokenizers                       | #
# ---------------------------------------------------------------------------- #

# ________________________________for Normalization_______________________________________________________

from khmernltk import word_tokenize as khmer_tokenize
import re
from khmerspell import khnormal
from convert_num2text import *
from convert_num2text.convertor import textNorm
from text.khmer_normalize_text import fix_virama

from khmernltk import word_tokenize as khmer_tokenize
import re
from khmerspell import khnormal


def khmer_normalization_v2(text):
    text = khnormal(text)
    text = fix_virama(text)
    text = re.sub(r'\s+', '', text).strip()
    text = text.replace('៖','').replace('\u200b','')


    # Tokenize and clean the text
    tokens = khmer_tokenize(text)
    tokens = ' '.join(tokens)
    tokens = re.sub(r'\s+', ' ', tokens).strip()
    tokens = re.sub(r'[\^\\*\+\?\{\}\[\]\\\|\(\)"]',' ', tokens)
    tokens = re.sub(r'[«»៕។▁]', ' ', tokens)

    # Add semicolon if needed
    punctuation = r"!?,.;។"
    if tokens and tokens[-1] not in punctuation:
        tokens += ';'

    return (tokens)


def text_normalization(text):
    # Split the text into words while preserving spaces
    words = text.split()

    # Process words individually
    normalized_words = []
    for word in words:
        if is_english(word):  
            normalized_words.append(eng_normalization(word))  # Normalize only English words
        else:
            normalized_words.append(khmer_normalization_v2(word))  # Normalize Khmer words

    return " ".join(normalized_words)  # Keep correct spacing

# _________________________________for convert num2text_______________________________________________________   
import re
from convert_num2text import *


def converting(text):
    print(f"[Normalized Text] {text}")
    # Fix spacing in commas caused by normalization (e.g., "1,255, 567" → "1,255,567")
    text = re.sub(r'(?<=\d),\s+(?=\d)', ',', text)
    text = re.sub(r'(?<=\d)\.\s+(?=\d)', '.', text)
    text = re.sub(r'(?<=[\d០-៩]),\s+(?=[\d០-៩])', ',', text)
    text = re.sub(r'(?<=[\d០-៩])\.\s+(?=[\d០-៩])', '.', text)
    text = re.sub(r'(?<=\d)\s*/\s*(?=\d)', '/', text)
    text = re.sub(r'(?<=\d)\s*-\s*(?=\d)', '-', text)
    # Normalize time spacing: "១៤: ៤៥" → "១៤:៤៥"
    text = re.sub(r'(?<=[\d០-៩])\s*:\s*(?=[\d០-៩])', ':', text)


    print ("before convert:",text)
    

    # Step 1: Convert Date
    text = re.sub(r'\b\d{1,2}/\d{1,2}/\d{4}\b', lambda m: safe_convert(m, convert_khmer_date_to_words, "Date"), text)
    text = re.sub(r'\b\d{1,2}-\d{1,2}-\d{4}\b', lambda m: safe_convert(m, convert_khmer_date_to_words, "Date"), text)

    # Step 2: Convert Time
    text = re.sub(r'\b\d{1,2}:\d{2}\b:\d{2}\b', lambda m: safe_convert(m, convert_khmer_time_to_words, "Time"), text)
    text = re.sub(r'\b\d{1,2}:\d{2}\b', lambda m: safe_convert(m, convert_khmer_time_to_words, "Time"), text)

    # Step 3: Convert Telephone
    text = re.sub(r'\b0\d{8,9}\b', lambda m: safe_convert(m, convert_khmer_telephone_to_words, "Telephone"), text)

    # Step 4: Convert Currency
    currency_pattern = r'[\$\៛\€\£\¥\₹\₱]\s?\d[\d,\.]*|\d[\d,\.]*\s?[\$\៛\€\£\¥\₹\₱]'
    text = re.sub(currency_pattern, lambda m: safe_convert(m, convert_currency_to_words, "Currency"), text)

    # Step 5: Convert Float/Big Numbers
    # number_pattern = r'\d{1,3}(?:,\d{3})+(?:\.\d+)?|\d+(?:\.\d+)?'
    number_pattern = r'[\d០-៩]{1,3}(?:,[\d០-៩]{3})+(?:[.,][\d០-៩]+)?|[\d០-៩]+(?:[.,][\d០-៩]+)?'
    text = re.sub(number_pattern, lambda m: safe_convert(m, handle_number, "Number"), text)

    return text

def khmer_to_arabic(number_str):
    """Convert Khmer numerals to Arabic numerals in a string."""
    khmer_digits = '០១២៣៤៥៦៧៨៩'
    arabic_digits = '0123456789'
    trans_table = str.maketrans(khmer_digits, arabic_digits)
    return number_str.translate(trans_table)

def safe_convert(match, func, label):
    try:
        original = match.group(0)
        converted = func(original)
        print(f"[{label}] {original} → {converted}")
        return converted
    except Exception as e:
        print(f"[{label} Error] {original} -> {e}")
        return original
    
def handle_number(number):
    khmer_digit_pattern = r'[០១២៣៤៥៦៧៨៩]'
    is_khmer = re.search(khmer_digit_pattern, number) is not None
    comma_count = number.count(',')
    has_dot = '.' in number
    has_decimal = has_dot or (comma_count == 1)  # ← only 1 comma = decimal in Khmer

    if is_khmer:
        number_arabic = khmer_to_arabic(number)

        if has_dot or (comma_count == 1 and '.' not in number):
            # Treat as float (e.g. "២៤.៥៦" or "២៤,៥៦")
            number_arabic = number_arabic.replace(',', '.')
            return convert_khmer_float_to_words(number_arabic)

        else:
            # Treat as big integer (e.g. "២៤,៦៧៨,៧៨៩")
            number_arabic = number_arabic.replace(',', '')
            return convert_number_to_words(number_arabic)

    else:
        # Arabic numbers
        if has_dot or (comma_count == 1 and '.' not in number):
            return convert_khmer_float_to_words(number.replace(',', '.'))
        else:
            return convert_number_to_words(number.replace(',', ''))

# ---------------------------------------------------------------------------- #
# |                              Emoji case                                  | #
# ---------------------------------------------------------------------------- #
import re

def remove_emoji (text):
    # Remove emojis
    # Emoji and emoji-like symbols (with variation selectors)
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # Emoticons
        "\U0001F300-\U0001F5FF"  # Symbols & Pictographs
        "\U0001F680-\U0001F6FF"  # Transport & Map Symbols
        "\U0001F1E0-\U0001F1FF"  # Flags
        "\U00002700-\U000027BF"  # Dingbats
        "\U0001F900-\U0001F9FF"  # Supplemental Symbols
        "\U00002600-\U000026FF"  # Miscellaneous Symbols
        "\U00002B00-\U00002BFF"  # Arrows
        "\U0001FA70-\U0001FAFF"  # Symbols Extended-A
        "\U000025A0-\U000025FF"  # Geometric Shapes
        "\u200d"                 # Zero Width Joiner
        "\ufe0f"                 # Variation Selector-16 (emoji modifier)
        "\u203c"                 # Double exclamation mark
        "\u2049"                 # Exclamation question mark
        "]+", flags=re.UNICODE)
    
    text = emoji_pattern.sub(r'', text)

    # Remove long repeated characters (like dots or ellipsis)
    text = re.sub(r'[.…•⋅·]{2,}', '', text)  # Removes 3 or more of '.', '…', '•', etc.
    text = emoji_pattern.sub(r'', text)
    # Remove hashtags
    text = re.sub(r'#', '', text)
    # Remove repeated punctuation like !! or .. or ……
    text = re.sub(r'([;.!?])\1{1,}', '', text)  # remove repeated punctuation
    text = re.sub(r'[…]{2,}', '', text)        # remove long ellipsis

    # Remove parentheses
    text = re.sub(r'[()]', '', text)
    
    return text.strip()

#__________________________________________for Khmer iteration_______________________________________________________

# def normalize_khmer_iteration(tokens):
#     new_tokens = []
#     i = 0
#     while i < len(tokens):
#         # Handle iteration on one word
#         if i >= 1 and tokens[i] == 'ៗ':
#             # Repeat the last word or syllable
#             last_word = new_tokens[-1]
#             new_tokens.append(last_word)
#             i += 1
#         else:
#             new_tokens.append(tokens[i])
#             i += 1
#     return " ".join(new_tokens)

# def lekto2text(text: str):
#     # Match any Khmer word or phrase followed by ៗ
#     lek_tos = re.findall(r'(([\u1780-\u17FF\s]+)ៗ)', text)
#     for full, phrase in lek_tos:
#         # Clean extra space
#         clean_phrase = phrase.strip()
#         repeated = f'{clean_phrase} {clean_phrase}'
#         # Replace only once per match
#         text = re.sub(re.escape(full), repeated, text, 1)
#     return text

#___________________________________________for Khmer iteration_______________________________________________________
# from khmernltk import word_tokenize as khmer_tokenize
# import re
# from khmerspell import khnormal

# def normalize_khmer_iteration(tokens):
#     new_tokens = []
#     i = 0
#     while i < len(tokens):
#         if i >= 1 and tokens[i] == 'ៗ':
#             last_word = new_tokens[-1]
#             new_tokens.append(last_word)
#             i += 1
#         else:
#             new_tokens.append(tokens[i])
#             i += 1
#     return " ".join(new_tokens)

# def lekto2text(text: str):
#     lek_tos = re.findall(r'(([\u1780-\u17FF\s]+)ៗ)', text)
#     for full, phrase in lek_tos:
#         clean_phrase = phrase.strip()
#         repeated = f'{clean_phrase} {clean_phrase}'
#         text = re.sub(re.escape(full), repeated, text, 1)
#     return text

# def khmer_normalization_v2(text):
#     # Step 1: Basic Khmer normalization
#     text = khnormal(text)
#     text = fix_virama(text)
#     text = re.sub(r'\s+', '', text).strip()
#     text = text.replace('៖','').replace('\u200b','')

#     # Step 2: Tokenize and clean
#     tokens = khmer_tokenize(text)  # returns a list of words/syllables
#     cleaned = ' '.join(tokens)
#     cleaned = re.sub(r'\s+', ' ', cleaned).strip()
#     cleaned = re.sub(r'[\^\\*\+\?\{\}\[\]\\\|\(\)"]',' ', cleaned)
#     cleaned = re.sub(r'[«»៕។▁]', ' ', cleaned).strip()

#     # Step 3: Add semicolon if needed
#     if cleaned and cleaned[-1] not in "!?,.;។":
#         cleaned += ';'

#     print(f"text after text_normalization: {cleaned}")

#     # Step 4: Normalize Khmer iteration from tokens
#     normalized = normalize_khmer_iteration(cleaned.split())
#     print(f"text after normalize_khmer_iteration: {normalized}")

#     # Step 5: Handle extra lekto using regex (just in case)
#     final = lekto2text(normalized)
#     print(f"text after lekto2text: {final}")

#     return final