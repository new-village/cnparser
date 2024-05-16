'''load.py
'''
import io
import re
import zipfile

import requests
import pandas as pd
from io import StringIO
from bs4 import BeautifulSoup

from cnparser.utility import load_config

def load(prefecture="All") -> pd.DataFrame:
    """Loads data for a specified prefecture.

    Args:
        prefecture (str): The name of the prefecture to load data for. Defaults to "All".

    Returns:
        DataFrame: A DataFrame containing the loaded data.
    """
    loader = ZipLoader()
    return loader.zip_load(_prefecture_2_file_id(prefecture))

def read_csv(file_path: str) -> pd.DataFrame:
    """Reads a CSV file from a specified path.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        DataFrame: A DataFrame containing the CSV data.
    """
    header = load_config("header")
    return pd.read_csv(file_path, encoding='utf-8', header=None, names=header, dtype='object')

def _prefecture_2_file_id(prefecture) -> str:
    """Converts prefecture name to a file ID using configuration.

    Args:
        prefecture (str): The prefecture name.

    Returns:
        str: The file ID associated with the prefecture.

    Raises:
        SystemExit: If the prefecture is not found in the configuration.
    """
    file_list = load_config("file_id")
    try:
        return file_list[prefecture.capitalize()]
    except KeyError as exp:
        raise SystemExit(f"Unexpected Key Value: {prefecture}") from exp

class ZipLoader():
    """Handles the loading and processing of zip files from a specified URL."""
    def __init__(self):
        self.url = "https://www.houjin-bangou.nta.go.jp/download/zenken/"
        self.key = "jp.go.nta.houjin_bangou.framework.web.common.CNSFWTokenProcessor.request.token"
        self.payload = {self.key: self._load_token(self.url, self.key), "event": "download"}

    def zip_load(self, file_id) -> pd.DataFrame:
        """Loads and processes a zip file from the server using a file ID.

        Args:
            file_id (str): The file ID to request the zip file.

        Returns:
            DataFrame: A DataFrame containing the data from the zip file.
        """
        contents = self._download_zip(file_id)
        csv_string = self._uncompress_file(contents)
        return self._convert_csv_2_df(csv_string)

    def _load_token(self, url, key) -> str:
        """Loads a security token from the server for requests.

        Args:
            url (str): The URL to load the token from.
            key (str): The key name of the token to retrieve.

        Returns:
            str: The token as a string.

        Raises:
            SystemExit: If the request fails.
        """
        try:
            response = requests.get(url, timeout=(3.0, 60.0))
            soup = BeautifulSoup(response.text, "html.parser")
            token = soup.find("input", {"name": key, "type": "hidden"})["value"]
        except requests.exceptions.RequestException as exp:
            raise SystemExit(f"Request to {url} has been failure") from exp
        return token

    def _download_zip(self, file_id) -> bytes:
        """Downloads a zip file from the server using the specified file ID.

        Args:
            file_id (str): The file ID to use for the download.

        Returns:
            bytes: The content of the zip file as bytes.

        Raises:
            SystemExit: If the request fails or the server responds with an error.
        """
        try:
            self.payload["selDlFileNo"] = file_id
            res = requests.post(self.url, params=self.payload, timeout=(3.0, 120.0))
        except requests.exceptions.RequestException as exp:
            print('Request is failure: Name, server or service not known')
            raise SystemExit("RequestsExceptions") from exp

        if res.status_code not in [200]:
            raise SystemExit('Request to ' + self.url + ' has been failed: ' + str(res.status_code))
        return res.content

    def _uncompress_file(self, content) -> StringIO:
        """Uncompresses the zip file content and extracts the CSV file.

        Args:
            content (bytes): The content of the zip file as bytes.

        Returns:
            StringIO: The CSV file content as a StringIO object.

        Raises:
            zipfile.BadZipFile: If the content is not a valid zip file.
        """
        try:
            zip_object = zipfile.ZipFile(io.BytesIO(content))
        except zipfile.BadZipFile:
            print("Failed to unzip content. The content may not be a valid zip file.")
            raise

        for file_name in zip_object.namelist():
            if not re.search(r'.*\.asc', file_name):
                txt = zip_object.open(file_name).read()
                return StringIO(txt.decode('utf-8'))

    def _convert_csv_2_df(self, csv_string) -> pd.DataFrame:
        """Converts a CSV string to a DataFrame using predefined headers.

        Args:
            csv_string (str): The CSV file content as a string.

        Returns:
            DataFrame: A DataFrame created from the CSV string.
        """
        header = load_config("header")
        return pd.read_csv(csv_string, encoding='utf-8', header=None, names=header, dtype='object')
