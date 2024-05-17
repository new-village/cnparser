import re
import pandas as pd
import unicodedata
import pykakasi
import warnings
import multiprocessing as mp

from cnparser.utility import load_config

def enrich(df: pd.DataFrame, *processes) -> pd.DataFrame:
    """
    Enriches the DataFrame with additional data processing functions specified by the user.

    Args:
        df (pd.DataFrame): The DataFrame to be processed.
        *processes (str): Variable length argument list of process names to apply.

    Returns:
        pd.DataFrame: The enriched DataFrame.
    """
    default_functions = {
        'enrich_kana': enrich_kana,
        'enrich_kind': enrich_kind,
    }

    if processes:
        default_functions = {key: default_functions[key] for key in processes if key in default_functions}

    if default_functions:
        return _parallel_process(df, default_functions)
    else:
        warnings.warn(f"No valid processing functions specified in {processes}. Returning the original DataFrame unchanged.")
        return df

def _parallel_process(df: pd.DataFrame, functions: dict) -> pd.DataFrame:
    """
    Processes the DataFrame in parallel using the specified functions.

    Args:
        df (pd.DataFrame): The DataFrame to be processed.
        functions (dict): A dictionary of functions to apply to the DataFrame.

    Returns:
        pd.DataFrame: The DataFrame after processing.
    """
    num_processes = mp.cpu_count()
    pool = mp.Pool(num_processes)
    df_split = [df.iloc[i::num_processes] for i in range(num_processes)]

    results = []
    for func_name in list(functions.keys()):
        result = pd.concat(pool.map(functions[func_name], df_split))
        results.append(result)
    pool.close()
    pool.join()
    return pd.concat(results)

def enrich_kana(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds a standardized furigana column to the DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame to be enriched.

    Returns:
        pd.DataFrame: The DataFrame with the 'std_furigana' column added.
    """
    df['std_furigana'] = df['name']
    df.loc[df['furigana'].notna(), 'std_furigana'] = df['furigana']
    df['std_furigana'] = df['std_furigana'].apply(_normalize_and_convert_kana)
    return df

def _normalize_and_convert_kana(text: str) -> str:
    """
    Normalizes and converts Japanese text to kana.

    Args:
        text (str): The text to be normalized and converted.

    Returns:
        str: The converted text in kana.
    """
    normalized_text = unicodedata.normalize('NFKC', text)
    legal_entity_regex = '|'.join(map(re.escape, load_config("legal_entity")))
    cleaned_text = re.sub(legal_entity_regex, '', normalized_text)
    kks = pykakasi.kakasi()
    return "".join(item['kana'] for item in kks.convert(cleaned_text))

def enrich_kind(df: pd.DataFrame) -> pd.DataFrame:
    """
    Placeholder function for enriching DataFrame with kind data.

    Args:
        df (pd.DataFrame): The DataFrame to be enriched.

    Returns:
        pd.DataFrame: The unchanged DataFrame as no implementation is provided.
    """
    return df
