'''load.py
'''
import csv
import io
import re
import zipfile
import requests
from bs4 import BeautifulSoup
from cnparser.utility import load_config

def bulk_load(prefecture="All"):
    """ Load Corporate Number Publication Site data.
    :param prefecture: prefecture name such as ALL, tokyo, tottori and shizuoka
    :return: :class:`Response <Response>` object
    """
    loader = ZipLoader()
    return loader.bulk_load(prefecture_2_file_id(prefecture))

def prefecture_2_file_id(prefecture) -> str:
    """ Convert prefecture name to the site defined file id.
    :param prefecture: STRING of prefecture name such as ALL, tokyo or tottori
    :return: Str object
    """
    # Load dict from config file
    file_list = load_config("file_id")
    # try to get file_id
    try:
        return file_list[prefecture.capitalize()]
    except KeyError as exp:
        raise SystemExit(f"Unexpected Key Value: {prefecture}") from exp

class ZipLoader():
    """ ZipLoader
    """
    def __init__(self):
        self.show = list()
        self.url = "https://www.houjin-bangou.nta.go.jp/download/zenken/"
        self.key = "jp.go.nta.houjin_bangou.framework.web.common.CNSFWTokenProcessor.request.token"
        self.payload = {self.key: self._load_token(self.url, self.key), "event": "download"}

    def bulk_load(self, file_id):
        """ Load Corporate Number Publication Site data.
        """
        # Download Corporate Number ZIP & Uncompression
        contents = self._download_zip(file_id)
        lines = self._uncompress_file(contents)
        # Convert string objects to List/Dict object
        self.show = self._convert_str_2_csv(lines)
        return self

    def _load_token(self, url, key) -> str:
        """ Load contents
        """
        try:
            # Request Contents
            response = requests.get(url, timeout=(3.0, 60.0))
            soup = BeautifulSoup(response.text, "html.parser")
            token = soup.find("input", {"name": key, "type": "hidden"})["value"]
        except requests.exceptions.RequestException as exp:
            raise SystemExit(f"Request to {url} has been failure") from exp
        return token

    def _download_zip(self, file_id) -> bytes:
        try:
            # Try to download ZIP file from JRDB with username and password.
            self.payload["selDlFileNo"] = file_id
            res = requests.post(self.url, params=self.payload, timeout=(3.0, 120.0))
        except requests.exceptions.RequestException as exp:
            # Exception error handling
            print('Request is failure: Name, server or service not known')
            raise SystemExit("RequestsExceptions") from exp

        # Response Status Confirmation
        if res.status_code not in [200]:
            # HTTP Response is not 200 (Normal)
            raise SystemExit('Request to ' + self.url + ' has been failure: ' + str(res.status_code))
        return res.content

    def _uncompress_file(self, content) -> list:
        # Create Zip Object from response strings
        zip_object = zipfile.ZipFile(io.BytesIO(content))

        # Uncompress ZIP files & union all files
        # if the Zip file has many text files, the script integrate files to single file.
        for file_name in zip_object.namelist():
            if not re.search(r'.*\.asc', file_name):
                txt = zip_object.open(file_name).read()
                lines = txt.decode().splitlines()
        return lines

    def _convert_str_2_csv(self, lines:list) -> list:
        """ Convert comma separated format string to dict nested list object.
        :param lines: List of comma separated string
        :return: List object
        """
        # Load header definition
        header = load_config("header")
        # Read comma separated format string
        reader = csv.DictReader(lines, fieldnames=header)
        return list(reader)
