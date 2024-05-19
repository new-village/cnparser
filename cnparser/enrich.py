import multiprocessing as mp
import re
import unicodedata
import warnings

import pandas as pd
from pandarallel import pandarallel
import pykakasi

from cnparser.utility import load_config

# Initialize libraries
pandarallel.initialize()
kks = pykakasi.kakasi()
legal_entity_regex = re.compile('|'.join(map(re.escape, load_config("legal_entity"))))
kind = load_config("kind")

def enrich(df: pd.DataFrame, *processes) -> pd.DataFrame:
    """
    Enriches the DataFrame with additional data processing functions specified by the user.

    Args:
        df (pd.DataFrame): The DataFrame to be processed.
        *processes (str): Variable length argument list of process names to apply.

    Returns:
        pd.DataFrame: The enriched DataFrame.
    """
    function_map = {
        'enrich_kana': enrich_kana,
        'enrich_kind': enrich_kind,
        'enrich_post_code': enrich_post_code,
    }

    valid_processes = []
    for proc in processes:
        if proc in function_map:
            valid_processes.append(proc)
        else:
            warnings.warn(f'No valid function name {proc}. Skip {proc} processing.')

    if len(valid_processes) > 0:
        selected_functions = [function_map[proc] for proc in valid_processes if proc in function_map]
    else:
        selected_functions = list(function_map.values())

    for func in selected_functions:
        df = func(df)

    return df

def enrich_kana(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds a standardized furigana column to the DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame to be enriched.

    Returns:
        pd.DataFrame: The DataFrame with the 'std_furigana' column added.
    """
    df['std_furigana'] = df['furigana'].where(df['furigana'].notna(), df['name'])
    df['std_furigana'] = df['std_furigana'].parallel_apply(_normalize_and_convert_kana)
    return df

def _normalize_and_convert_kana(text: str) -> str:
    """
    Normalizes and converts Japanese text to kana.

    Args:
        text (str): The text to be normalized and converted.

    Returns:
        str: The converted text in kana.
    """
    if re.fullmatch(r"[ァ-ヴー]+", text):
        return text
    else:
        normalized_text = unicodedata.normalize('NFKC', text)
        cleaned_text = legal_entity_regex.sub('', normalized_text)
        return "".join(item['kana'] for item in kks.convert(cleaned_text))

def enrich_kind(df: pd.DataFrame) -> pd.DataFrame:
    """
    Maps the 'kind' column of the DataFrame to a standardized legal entity description.

    Args:
        df (pd.DataFrame): The DataFrame to be enriched.

    Returns:
        pd.DataFrame: The DataFrame with the 'std_legal_entity' column added, containing standardized legal entity descriptions.
    """
    df['std_legal_entity'] = df['kind'].map(kind)
    return df

def enrich_post_code(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds a standardized postal code column to the DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame to be enriched.

    Returns:
        pd.DataFrame: The DataFrame with the 'std_post_code' column added, where postal codes are formatted as 'XXX-XXX'.
    """
    df['std_post_code'] = df['post_code'].parallel_apply(lambda x: f"{str(x)[:3]}-{str(x)[3:]}" if pd.notna(x) else None)
    return df
