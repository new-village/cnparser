from concurrent.futures import ThreadPoolExecutor
import pykakasi  # Library for generating furigana
import re  # Regular expression library
import jaconv  # Japanese character conversion library

from cnparser.utility import load_config

# Load dictionary from configuration file
eng_kana = load_config("eng_kana")

def copy_name_to_efurigana(record):
    """
    Copies the value of the 'name' key to the 'e_furigana' key in the record.
    
    Args:
        record (dict): A dictionary containing at least the 'name' key.
    
    Returns:
        dict: The updated dictionary with 'e_furigana' key set.
    """
    record['e_furigana'] = record.get('name', '')
    return record

def generate_furigana(record):
    """
    Generates furigana for the Japanese text stored in 'e_furigana' key of the record.
    
    Args:
        record (dict): A dictionary with the 'e_furigana' key containing Japanese text.
    
    Returns:
        dict: The updated dictionary with 'e_furigana' key updated to its furigana.
    """
    kks = pykakasi.kakasi()
    result = kks.convert(record['e_furigana'])
    record['e_furigana'] = "".join(item['kana'] for item in result)
    return record

def remove_legal_entity(record):
    """
    Removes legal entity suffixes from the 'e_furigana' key in the record.
    
    Args:
        record (dict): A dictionary with the 'e_furigana' key potentially containing legal entity suffixes.
    
    Returns:
        dict: The updated dictionary with legal entity suffixes removed from 'e_furigana'.
    """
    legal_entities = ['株式会社', '有限会社', '合名会社', '合資会社', '合同会社', '特定目的会社']
    pattern = r'({})'.format('|'.join(legal_entities))
    record['e_furigana'] = re.sub(pattern, '', record['e_furigana'])
    return record

def normalize_name(record):
    """
    Normalizes and converts the 'e_furigana' key to uppercase using NFKC normalization.
    
    Args:
        record (dict): A dictionary with the 'e_furigana' key containing Japanese text.
    
    Returns:
        dict: The updated dictionary with 'e_furigana' normalized and converted to uppercase.
    """
    record['e_furigana'] = jaconv.normalize(record['e_furigana'], 'NFKC').upper()
    return record

def convert_to_katakana(record):
    """
    Converts characters in 'e_furigana' from the dictionary mapping defined in 'eng_kana'.
    
    Args:
        record (dict): A dictionary with the 'e_furigana' key containing text to be converted.
    
    Returns:
        dict: The updated dictionary with 'e_furigana' converted to katakana where applicable.
    """
    for key, value in eng_kana.items():
        record['e_furigana'] = record['e_furigana'].replace(key, value)
    return record

def enrich_kana(records):
    """
    Processes a list of records in parallel to generate furigana.
    
    Args:
        records (list of dict): A list of dictionaries to be processed.
    
    Returns:
        list of dict: The list of dictionaries with updated 'e_furigana' keys.
    """
    with ThreadPoolExecutor() as executor:
        funcs = [copy_name_to_efurigana, normalize_name, remove_legal_entity, generate_furigana, convert_to_katakana]
        for func in funcs:
            records = list(executor.map(func, records))
    return records

