'''load.py
'''
import io
import re
import zipfile
import requests
from bs4 import BeautifulSoup

def bulk_load():
    """ Load Corporate Number Publication Site data.
    :param prefecture: prefecture name such as ALL, tokyo, tottori and shizuoka
    :return: :class:`Response <Response>` object
    """
    loader = ZipLoader()
    return loader.bulk_load()

class ZipLoader():
    """ ZipLoader
    """
    def __init__(self):
        self.data = list()
        self.url = "https://www.houjin-bangou.nta.go.jp/download/zenken/"
        self.key = "jp.go.nta.houjin_bangou.framework.web.common.CNSFWTokenProcessor.request.token"
        # self.payload = {self.token_key: self._load_token(self.url, self.token_key), "event": "download", "selDlFileNo": "17856"}
        self.payload = {self.key: self._load_token(self.url, self.key), "event": "download", "selDlFileNo": "17955"}

    def bulk_load(self):
        """ Load Corporate Number Publication Site data.
        """
        # Download Corporate Number ZIP & Uncompression
        contents = self._download_zip()
        csv = self._uncompress_file(contents)
        # TODO: Parse text file to Dict format
        self.data = csv
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

    def _download_zip(self) -> bytes:
        try:
            # Try to download ZIP file from JRDB with username and password.
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
