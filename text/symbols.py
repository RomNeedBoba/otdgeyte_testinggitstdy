"""
Set of symbols
"""
_punctuation = ';:,.!?¡¿—…"«»“”/'


"""
Special symbols
"""
# Define special symbols and indices
special_symbols = ["<pad>", "<unk>", "<bos>", "<eos>", "<space>", "<laugh>"]
PAD_ID, UNK_ID, BOS_ID, EOS_ID = 0, 1, 2, 3

# Define the set of symbols
symbols = list(_punctuation) + special_symbols
# Define the set of symbols
symbols_1 = list(_punctuation) + special_symbols