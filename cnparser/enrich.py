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
        'standardization': standardization,
        'enrich_kana': enrich_kana,
        'enrich_kind': enrich_kind,
        'enrich_post_code': enrich_post_code,
    }

    valid_processes = [standardization]
    for proc in processes:
        if proc in function_map:
            valid_processes.append(proc)
        else:
            warnings.warn(f'No valid function name {proc}. Skip {proc} processing.')

    if len(valid_processes) == 1:
        selected_functions = list(function_map.values())
    else:
        selected_functions = [function_map[proc] for proc in valid_processes if proc in function_map]

    for func in selected_functions:
        df = func(df)

    return df

def standardization(df: pd.DataFrame) -> pd.DataFrame:
    """
    Converts all string columns in the DataFrame to half-width.

    Args:
        df (pd.DataFrame): The DataFrame to be converted.

    Returns:
        pd.DataFrame: The DataFrame with all string columns converted to half-width.
    """
    for column in df.columns:
        df[column] = df[column].parallel_apply(lambda x: _convert_to_half_width(x) if isinstance(x, str) else x)
    return df

def enrich_kana(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds a standardized furigana column to the DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame to be enriched.

    Returns:
        pd.DataFrame: The DataFrame with the 'std_furigana' column added.
    """
    df['furigana'] = df['furigana'].where(df['furigana'].notna(), df['name'])
    df['furigana'] = df['furigana'].parallel_apply(_normalize_and_convert_kana)
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
        cleaned_text = legal_entity_regex.sub('', text)
        return "".join(item['kana'] for item in kks.convert(cleaned_text))

def enrich_kind(df: pd.DataFrame) -> pd.DataFrame:
    """
    Maps the 'kind' column of the DataFrame to a standardized legal entity description.

    Args:
        df (pd.DataFrame): The DataFrame to be enriched.

    Returns:
        pd.DataFrame: The DataFrame with the 'std_legal_entity' column added, containing standardized legal entity descriptions.
    """
    df['legal_entity'] = df['kind'].map(kind)
    return df

def enrich_post_code(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds a standardized postal code column to the DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame to be enriched.

    Returns:
        pd.DataFrame: The DataFrame with the 'std_post_code' column added, where postal codes are formatted as 'XXX-XXX'.
    """
    df['post_code'] = df['post_code'].parallel_apply(lambda x: f"{str(x)[:3]}-{str(x)[3:]}" if pd.notna(x) else None)
    return df

def _convert_to_half_width(text: str) -> str:
    """
    Converts full-width alphanumeric characters and symbols to half-width.

    Args:
        text (str): The text to be converted.

    Returns:
        str: The converted text in half-width.
    """
    half_width_text = unicodedata.normalize('NFKC', text)
    return half_width_text