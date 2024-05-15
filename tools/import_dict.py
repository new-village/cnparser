import os
import sys
import re
import json

def get_file_path():
    """ Get the file path from command line arguments, return default path if none provided.
    :return: The file path as a string.
    """
    path = "".join(sys.argv[1:])
    default_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bep-eng.dic")
    return path if path else default_path

def load_file_contents(file_path):
    """ Load the contents of a file.
    :param file_path: The path to the file as a string.
    :return: The contents of the file as a string, or None if an error occurs.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"Error reading file: {e}")

def parse_text_to_dict(text):
    """ Parse text and convert it into a dictionary.
    :param text: The text to parse as a string.
    :return: A dictionary with words as keys and their translations as values.
    """
    lines = [line for line in text.strip().split('\n') if line and not line.startswith('#')]
    return {line.split()[0]: " ".join(line.split()[1:]) for line in lines if len(line.split()) >= 2}

def apply_regex_to_values(dictionary):
    """ Apply regular expressions to the values in the dictionary.
    :param dictionary: The dictionary to process.
    :return: The dictionary with modified values.
    """
    patterns = [
        (r'ドゥ$', 'ド'), 
        (r'トゥ$', 'ト'), 
        (r'(?<=[ドト])ゥ(?!ー)', ''), 
        (r'(?=[ドト])ゥ(?<!ー)', ''), 
        (r'(?<=[キシチニヒミリィ])イ', 'ー'), 
        (r'(?<=[ァゥェォ])ィ', 'イ'), 
        (r'イション', 'ーション'), 
        (r'ォウ', 'ォー'), 
        (r'スィ', 'シー'), 
        (r'ロウ', 'ロー'), 
        (r'゛', ''), 
        (r'ウカ', 'ーカ'), 
        (r'トギャザー', 'トゥゲザー'), 
        (r'ボキャビュラリー', 'ボキャブラリー'), 
        (r'ーー', 'ー')
    ]
    for key, value in dictionary.items():
        for pattern, replacement in patterns:
            value = re.sub(pattern, replacement, value)
        dictionary[key] = value
   
    return dictionary

def sort_dict_by_key_length(dictionary):
    """ Sort the dictionary by the length of the keys and alphabetically.
    :param dictionary: The dictionary to sort.
    :return: A new dictionary sorted by key length and alphabetically.
    """
    return dict(sorted(dictionary.items(), key=lambda item: (len(item[0]), item[0]), reverse=True))

def remove_single_char_keys(dictionary):
    """ Remove entries from the dictionary where the key is a single character.
    :param dictionary: The dictionary to process.
    :return: A new dictionary with single character keys removed.
    """
    return {k: v for k, v in dictionary.items() if len(k) > 1}

def add_custom_entries(dictionary):
    """ Add custom entries to the dictionary.
    :param dictionary: The dictionary to update.
    :return: The updated dictionary.
    """
    custom_entries = {
        '&': 'アンド', 
        'COPEL': 'コペル', 
        'OCEANS': 'オーシャンズ',
        'SOLUTIONS': 'ソリューションズ', 
        'HAP':'ハップ', 
        'SAS': 'サス', 
        'SAP': 'エスエーピー'
    }
    dictionary.update(custom_entries)
    return dictionary

def save_dict_as_json(dictionary):
    """ Save the dictionary as a JSON file.
    :param dictionary: The dictionary to save.
    """
    file_path = os.path.join(os.path.dirname(__file__), '../cnparser/config/eng_kana.json')
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(dictionary, file, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    path = get_file_path()
    text = load_file_contents(path)
    dictionary = parse_text_to_dict(text)
    dictionary = apply_regex_to_values(dictionary)
    dictionary = remove_single_char_keys(dictionary)
    dictionary = add_custom_entries(dictionary)
    dictionary = sort_dict_by_key_length(dictionary)
    save_dict_as_json(dictionary)

