"""
Cleaners are transformations that run over the input text at both training and eval time.

Cleaners can be selected by passing a comma-delimited list of cleaner names as the "cleaners"
hyperparameter.
"""

import re
from typing import List
from torchtext.vocab import build_vocab_from_iterator
from phonemizer import phonemize
from khmerphonemizer import phonemize
from phonemizer.separator import Separator


from text.normalize_numbers import normalize_numbers

from text.symbols import _punctuation, PAD_ID, UNK_ID, BOS_ID, EOS_ID


_whitespace_re = re.compile(r"\s+")
_preserved_symbols_re = re.compile(rf"[{_punctuation}]|<.*?>")
separator = Separator(word="<space>", phone=" ")


# ---------------------------------------------------------------------------- #
# |                                Text cleaners                             | #
# ---------------------------------------------------------------------------- #
def lowercase(text: str, *args, **kwargs):
    return text.lower()


def collapse_whitespace(text: str, *args, **kwargs):
    return re.sub(_whitespace_re, " ", text)


def expand_numbers(text: str, *args, **kwargs):
    return normalize_numbers(text)


# def phonemize_text(text: List[str] | str, *args, language="en-us", **kwargs):
#     return phonemize(text, language=language, backend="espeak", separator=separator, strip=True, preserve_punctuation=True, punctuation_marks=_preserved_symbols_re, with_stress=True, njobs=8)

# ---------------------------------------------------------------------------- #
# |                                Khmer Phonemizer                          | #
# ---------------------------------------------------------------------------- #
import re
from khmerphonemizer import phonemize

def phonemize_text(text: list[str] | str, *args, **kwargs) -> str:
    """
    Converts Khmer text (string or list of strings) to a phoneme sequence using khmerphonemizer.
    Preserves non-Khmer symbols and inserts <space> between phoneme units.

    Parameters:
    - text: str | list[str] -- input Khmer sentence(s)
    
    Returns:
    - str: space-separated phonemes with <space> between meaningful tokens
    """
    if isinstance(text, list):
        text = " ".join(text)

    if not text.strip():
        return ''

    # Apply Khmer phonemization
    result = phonemize(text)

    # Get the list of phonemes from the tuple
    if isinstance(result, tuple) and len(result) > 1:
        phoneme_list = result[1]
    else:
        return ''

    processed = []
    for item in phoneme_list:
        if item in ['', ' ']:
            processed.append('<space>')
        else:
            processed.append(' '.join(item))  # Insert space between characters in each unit

    return ' '.join(processed)

def add_spaces(text: str, *args, **kwargs):
    spaced_text = re.sub(_preserved_symbols_re, r" \g<0> ", text)
    cleaned_text = re.sub(_whitespace_re, " ", spaced_text)
    return cleaned_text.strip()

# ---------------------------------------------------------------------------- #
# |                               Token cleaners                             | #
# ---------------------------------------------------------------------------- #


def tokenize_text(text: str, vocab: build_vocab_from_iterator, *args, **kwargs):
    tokens = text.split()
    return vocab(tokens)


def add_bos_eos(tokens: List[int], *args, **kwargs):
    return [BOS_ID] + tokens + [EOS_ID]


def add_blank(tokens: List[int], *args, **kwargs):
    result = [PAD_ID] * (len(tokens) * 2 + 1)
    result[1::2] = tokens
    return result


def delete_unks(tokens: List[int], *args, **kwargs):
    return [token for token in tokens if token != UNK_ID]


def detokenize_sequence(sequence: List[int], vocab: build_vocab_from_iterator, *args, **kwargs):
    return "".join(vocab.lookup_tokens(sequence))







# ---------------------------------------------------------------------------- #
# |                                Khmer token                          | #
# ---------------------------------------------------------------------------- #

# def tokenize_text(text: str, vocab: build_vocab_from_iterator, *args, **kwargs):
from text.khmer_normalize_text import fix_virama, replace_percentage,is_english, eng_normalization, khmer_normalization

def normalize_text(text: str, vocab: build_vocab_from_iterator, *args, **kwargs):
    if is_english(text):
        return eng_normalization(text)
    else:
        text = replace_percentage(text)
        text = fix_virama(text)
        return khmer_normalization(text)
    
# ---------------------------------------------------------------------------- #
# |                                Khmer token v2                         | #
# ---------------------------------------------------------------------------- #


from text.khmer_normalize_text import text_normalization, replace_percentage, fix_virama, converting, remove_emoji
# from text.khmer_normalize_text import text_normalization, replace_percentage

import re

def kh_normalization(text: str, vocab: build_vocab_from_iterator, *args, **kwargs):
    text = text_normalization(text)
    print("text after text_normalization: ", text)
    # text = normalize_khmer_iteration(text.split())
    # print("text after normalize_khmer_iteration: ", text)
    # text = lekto2text(text)
    # print("text after lekto2text: ", text)
    text = converting(text)
    print("text after converting: ", text)
    text = replace_percentage(text)
    print("text after replace_percentage: ", text)
    text = remove_emoji(text)
    print("text after remove_emoji: ", text)
     # Clean all repeated semicolons in text (e.g., ';;' -> ';')
    text = re.sub(r";{2,}", ";", text)
    return text


# import re

# def kh_normalization(text):
#     text = text_normalization(text)
#     print("text after text_normalization: ", text)
#     text = fix_virama(text)
#     print("text after fix_virama: ", text)
#     text = converting(text)
#     print("text after converting: ", text)
#     text = replace_percentage(text)
#     print("text after replace_percentage: ", text)
    
#     # Ensure semicolon at the end (optional)
#     text = text.strip()
#     if not text.endswith(';'):
#         text += ';'

#     return text


# def kh_normalization(text):
#     text = text_normalization(text)
#     print("text after text_normalization: ", text)
#     text = fix_virama(text)
#     print("text after fix_virama: ", text)
#     text = converting(text)
#     print("text after converting: ", text)
#     text = replace_percentage(text)
#     print("text after replace_percentage: ", text)
#     # Remove ;, ., and all whitespace
#     # text = re.sub(r'[.]', '', text)
#     return text



# def normalize_text(text: str, vocab: build_vocab_from_iterator, *args, **kwargs):
#     if is_english(text):
#         return eng_normalization(text).replace(";", "")
#     else:
#         text = replace_percentage(text)
#         text = fix_virama(text)
#         return khmer_normalization(text).replace(";", "")

 
# # from text.khmer_normalize_text import text_normalization, replace_percentage, fix_virama, converting
# from text.khmer_normalize_text import text_normalization, replace_percentage

# import re

# import re

# def kh_normalization(text):
#     text = text_normalization(text)
#     print("text after text_normalization: ", text)
#     # text = converting(text)
#     print("text after converting: ", text)
#     text = replace_percentage(text)
#     print("text after replace_percentage: ", text)
#     # Remove ;, ., and all whitespace
#     # text = re.sub(r'[.]', '', text)
#     return text
