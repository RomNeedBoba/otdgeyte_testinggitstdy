from .convertor import *


#     # Step 1: Check if the number is in English or Khmer
# def check_type_of_num(text):
#     if is_num_en(text):  # English number
#         return "English"
#     elif is_num_km(text):  # Khmer number
#         return "Khmer"
#     else:
#         return "Invalid input: Not a valid number in either English or Khmer."

# def check_float_int_num(text):
#     # Step 2: Check if the number is float or Khmer
#     num_type = check_type_of_num(text)
#     if num_type == "English":
#         return is_float_en(text)
#     elif num_type == "Khmer":
#         return is_float_km(text)
#     else:
#         return num_type  # Return the error message
    
#####################################################
## for date conversion to words

def convert_khmer_date_to_words(date_str: str, full_word: bool = False) -> str:
    """
    Converts a date string (in Khmer or English numerals) to its Khmer word representation.
    Automatically detects and converts English numerals to Khmer if necessary.
    
    Args:
        date_str (str): Date string in either Khmer or English numerals (e.g., ០១-០២-២០២៤ or 01-02-2024)
        full_word (bool): Whether to use full word forms in output.
    
    Returns:
        str: Date in Khmer words.
    
    Raises:
        Exception: If input date (after conversion) is not a valid Khmer date.
    """
    # Step 1: Detect if date is in English and convert it to Khmer numerals
    if is_num_en(date_str):
        date_km = num_en2km(date_str)
    else:
        date_km = date_str

    # Step 2: Validate Khmer date format
    if not is_date_km(date_km):
        raise Exception(f'Invalid Khmer date format: {date_km}')

    # Step 3: Convert to Khmer words
    return date2word(date_km, full_word=True)

########################################################
## time conversion to words

def convert_khmer_time_to_words(times: str) -> str:
    """Convenience function to convert Khmer time to words"""
    # Step 1: Detect if date is in English and convert it to Khmer numerals
    if is_num_en(times):
        time_km = num_en2km(times)
    else:
        time_km = times

    # Step 2: Validate Khmer time format
    if not is_time_km(time_km):
        raise Exception(f'Invalid Khmer time format: {time_km}')    

    # Step 3: Convert to Khmer words
    return time2word(time_km)

#########################################################
## convert from telephone number to words

def convert_khmer_telephone_to_words(phone: str) -> str:
    """
    Convert a telephone number to Khmer words.
    
    Steps:
    1. If the number is in English (e.g., "0123456789"), convert it to Khmer using en2km().
    2. Check if the converted number is a valid telephone number using is_to_te().
    3. Convert it to Khmer words using digits2word().
    """
    # Step 1: Convert English digits to Khmer if needed
    if is_num_en(phone):
        phone_km = num_en2km(phone)
    else:
        phone_km = phone

    # Step 2: Validate telephone number
    if not is_tel_num(phone_km):
        raise Exception(f"Invalid telephone number format: {phone_km}")
    
    # Step 3: Convert digits to Khmer words
    return digits2word(phone_km)

##########################################################
## convert from float to text 

def convert_khmer_float_to_words(number: str) -> str:
    """
    Convert a float number to Khmer words.
    
    Steps:
    - If the number is in English float format:
        1. Convert it to Khmer numerals using num_en2km.
        2. Convert to Khmer words using num2word.
    
    - If the number is in Khmer float format:
        1. Convert it to English using km2en.
        2. Convert it to Khmer numerals using num_en2km.
        3. Convert to Khmer words using num2word.
    """
    if is_float_en(number):
        # English float -> Khmer numerals
        number_km = num_en2km(number)
    elif is_float_km(number):
        # Khmer float -> English -> Khmer numerals
        number_km = num_en2km(km2en(number))
    else:
        raise Exception(f"Invalid float number format: {number}")

    # Convert Khmer numeral float to words
    return num2word(number_km)

############################################################
## convert from integer to text

def convert_number_to_words(num_str: str) -> str:
    """
    Converts a date string (in Khmer or English numerals) to its Khmer word representation.
    Automatically detects and converts English numerals to Khmer if necessary.
    
    Args:
        date_str (str): Date string in either Khmer or English numerals (e.g., ០១-០២-២០២៤ or 01-02-2024)
        full_word (bool): Whether to use full word forms in output.
    
    Returns:
        str: Date in Khmer words.
    
    Raises:
        Exception: If input date (after conversion) is not a valid Khmer date.
    """
    # Step 1: Detect if date is in English and convert it to Khmer numerals
    if is_num_en(num_str):
        num_km = en2km(num_str)
    else:
        num_km = num_str

    # Step 3: Convert to Khmer words
    return num2word(num_km)

############################################################
## convert from currency to text

def convert_currency_to_words(num_str: str) -> str:
    return textNorm(num_str)




