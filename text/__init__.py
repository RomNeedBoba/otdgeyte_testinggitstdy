from typing import List
from text.cleaners import fix_virama, replace_percentage
from text.cleaners import eng_normalization, khmer_normalization,is_english
from text import cleaners
from torchtext.vocab import Vocab



def tokenizer(text: str, vocab: Vocab, cleaner_names: List[str], language="en-us", cleaned_text=False) -> List[int]:
    """Converts a string of text to a sequence of IDs corresponding to the symbols in the text.
    Args:
        text: string to convert to a sequence of IDs
        cleaner_names: names of the cleaner functions from text/cleaners.py
        language: language ID from https://github.com/espeak-ng/espeak-ng/blob/master/docs/languages.md
        cleaned_text: whether the text has already been cleaned
    Returns:
        List of integers corresponding to the symbols in the text
    """
    if not cleaned_text:
        return _clean_text(text, vocab, cleaner_names, language=language)
    else:
        return list(map(int, text.split("\t")))


def detokenizer(sequence: List[int], vocab: Vocab) -> str:
    """Converts a sequence of tokens back to a string"""
    return "".join(vocab.lookup_tokens(sequence))



def _clean_text(text: str, vocab: Vocab, cleaner_names: List[str], language="en-us") -> str:
    for name in cleaner_names:
        cleaner = getattr(cleaners, name)
        assert callable(cleaner), f"Unknown cleaner: {name}"
        text = cleaner(text, vocab=vocab, language=language)
    return text

# def _clean_text(text: str, cleaner_names: List[str], language="en-us") -> str:
#     for name in cleaner_names:
#         cleaner = getattr(cleaners, name)
#         assert callable(cleaner), f"Unknown cleaner: {name}"
#         text = cleaner(text, language=language)
#     return text


# def normalize_abbreviation(text):
#     """
#     Full pipeline to normalize Khmer abbreviations and virama in text.
#     """
#     if isinstance(text, list):
#         text = " ".join(str(x) for x in text)  # 🔧 make sure all elements are strings

#     text = fix_virama(text)
#     text = replace_percentage(text)
#     return text



# def kh_tokenize_text(text):
#      # First, normalize Khmer abbreviations and virama
#     text = normalize_abbreviation(text)

#     # Split the text into words while preserving spaces
#     words = text.split()

#     # Process words individually
#     normalized_words = []
#     for word in words:
#         if is_english(word):  
#             normalized_words.append(eng_normalization(word))  # Normalize only English words
#         else:
#             normalized_words.append(khmer_normalization(word))  # Normalize Khmer words

#     return " ".join(normalized_words)  # Keep correct spacing


# def kh_tokenize_text(text: str, vocab: Vocab, cleaner_names: List[str], language="kh", cleaned_text=False) -> List[int]:
#     """
#     Tokenizes Khmer and English mixed text into a list of vocab IDs.
#     """
#     if not cleaned_text:
#         # First, normalize Khmer abbreviations and virama
#         text = normalize_abbreviation(text)

#         # Split the text into words while preserving spaces
#         words = text.split()

#         # Normalize each word depending on its language
#         normalized_words = []
#         for word in words:
#             if is_english(word):
#                 normalized_words.append(eng_normalization(word))
#             else:
#                 normalized_words.append(khmer_normalization(word))

#         # Rejoin into cleaned text
#         text = " ".join(normalized_words)

#     # Convert to vocab IDs
#     return [vocab[symbol] for symbol in text if symbol in vocab]

# def tokenizer(
#     text: str,
#     vocab: Vocab,
#     cleaner_names: List[str],
#     language: str = "kh",
#     cleaned_text: bool = False
# ) -> List[int]:
#     """
#     Converts a string of text to a sequence of vocab IDs.

#     Args:
#         text: string to convert
#         vocab: vocabulary object mapping symbols to IDs
#         cleaner_names: names of the cleaner functions from text/cleaners.py
#         language: language code (e.g., "en-us", "kh")
#         cleaned_text: whether the text has already been cleaned

#     Returns:
#         List[int]: List of vocab IDs
#     """
#     if not cleaned_text:
#         if language.lower().startswith("kh"):
#             # Normalize Khmer abbreviations and virama
#             text = normalize_abbreviation(text)

#             # Split text into words
#             words = text.split()

#             # Normalize each word based on detected language
#             normalized_words = []
#             for word in words:
#                 if is_english(word):
#                     normalized_words.append(eng_normalization(word))
#                 else:
#                     normalized_words.append(khmer_normalization(word))

#             text = " ".join(normalized_words)

#         else:
#             # Use default text cleaner for non-Khmer languages
#             return _clean_text(text, vocab, cleaner_names, language=language)

#     # Convert text to vocab IDs
#     return [vocab[symbol] for symbol in text if symbol in vocab] if not cleaned_text else list(map(int, text.split("\t")))


# from typing import List
# from torchtext.vocab import Vocab  # or your actual vocab class

# def tokenizer(
#     text: str,
#     vocab: Vocab,
#     cleaner_names: List[str],
#     language: str = "kh",
#     cleaned_text: bool = False
# ) -> List[int]:
#     """
#     Converts a string of text to a sequence of vocab IDs.

#     Args:
#         text: string to convert
#         vocab: vocabulary object mapping symbols to IDs
#         cleaner_names: names of the cleaner functions from text/cleaners.py
#         language: language code (e.g., "en-us", "kh")
#         cleaned_text: whether the text has already been cleaned

#     Returns:
#         List[int]: List of vocab IDs
#     """
#     if cleaned_text:
#         # Expect tab-separated list of token IDs
#         try:
#             return list(map(int, text.strip().split("\t")))
#         except ValueError:
#             raise ValueError("Expected tab-separated string of integers when cleaned_text=True")

#     if language.lower().startswith("kh"):
#         # Normalize Khmer abbreviations and virama
#         text = normalize_abbreviation(text)

#         # Split text into words
#         words = text.split()

#         # Normalize each word based on language
#         normalized_words = []
#         for word in words:
#             if is_english(word):
#                 normalized_words.extend(eng_normalization(word).split())  # returns str
#             else:
#                 normalized_words.extend(khmer_normalization(word).split())  # returns str

#         tokens = normalized_words
#     else:
#         # Fallback to default cleaner
#         tokens = _clean_text(text, vocab, cleaner_names, language=language).split()

#     # Convert tokens to vocab IDs
#     return [vocab[token] for token in tokens if token in vocab]


if __name__ == "__main__":
    from utils.task import load_vocab

    vocab = load_vocab("datasets/ljs_base/vocab.txt")
    cleaner_names = ["phonemize_text", "add_spaces", "tokenize_text", "delete_unks", "add_bos_eos", "detokenize_sequence"]
    text = "Well, I like pizza. <laugh> You know … Who doesn't like pizza? <laugh>"
    print(tokenizer(text, vocab, cleaner_names, language="en-us", cleaned_text=False))
