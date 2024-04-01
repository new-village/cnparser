'''load.py
'''
import csv
import io
import os
import re
import json
import zipfile
import datetime

import requests
from bs4 import BeautifulSoup
from functools import partial
from concurrent.futures import ProcessPoolExecutor
from normalize_japanese_addresses import normalize

import cnparser
from cnparser.utility import load_config

api_location = 'file://' + os.path.dirname(cnparser.__file__) + '/config/api/ja'

def bulk_load(prefecture="All"):
    """ Load Corporate Number Publication Site data.
    :param prefecture: prefecture name such as ALL, tokyo, tottori and shizuoka
    :return: :class:`List <list>` object
    """
    loader = ZipLoader()
    return loader.bulk_load(_prefecture_2_file_id(prefecture))

def bulk_enrich(data, export_file=None):
    """ 
    Enriches the data from the Corporate Number Publication Site.
    Accepts either a path to a CSV file or a list of data, and returns a list of data with normalized address information.

    :param data: Path to a CSV file or a list of corporate data
    :return: A list of corporate data with normalized address information
    """
    if isinstance(data, str) and ".csv" in data:
        data = _read_csv_file(data)
    elif not isinstance(data, list):
        raise ValueError("Invalid argument type. Argument must be a .csv file path or a list.")

    normalized_data = _normalize_address(data)
    if export_file:
        with open(export_file, 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=normalized_data[0].keys())
            writer.writeheader()
            writer.writerows(normalized_data)

    return normalized_data

def _read_csv_file(file_path: str) -> list:
    """ Read a CSV file and return a list of dictionaries """
    data_list = []
    headers = load_config("header")
    with open(file_path, 'r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        cnt = 1
        for row in csv_reader:
            cnt = cnt + 1
            # rowの長さがheadersの長さと一致するか確認
            if len(row) != len(headers):
                print(f"Warning: Row {cnt} skipped due to mismatched length. Expected {len(headers)}, got {len(row)}.")
                continue  # この行をスキップ
            data_list.append({headers[i]: row[i] for i in range(len(headers))})
    return data_list

def _prefecture_2_file_id(prefecture) -> str:
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

def update_progress_and_normalize(corp, index, total_lines, progress_interval):
    if index % progress_interval == 0:
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"{current_time} - Processing progress: {int((index / total_lines) * 100)}% complete")
    addr = str(corp['prefecture_name']) + str(corp['city_name']) + str(corp['street_number'])
    corp.update(normalize(addr, endpoint=api_location))
    return corp

def _normalize_address(lines):
    total_lines = len(lines)
    print(f"Processing {total_lines} records.")
    progress_interval = total_lines // 10

    # functools.partialを使用して、追加の引数を設定
    func = partial(update_progress_and_normalize, total_lines=total_lines, progress_interval=progress_interval)

    with ProcessPoolExecutor(max_workers=os.cpu_count()) as executor:
        # executor.mapに渡すために、funcを使用
        lines = list(executor.map(func, lines, range(total_lines)))
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{current_time} - Processing progress: 100% complete")
    
    return lines

class ZipLoader():
    """ ZipLoader
    """
    def __init__(self):
        self.show = list()
        self.url = "https://www.houjin-bangou.nta.go.jp/download/zenken/"
        self.key = "jp.go.nta.houjin_bangou.framework.web.common.CNSFWTokenProcessor.request.token"
        self.payload = {self.key: self._load_token(self.url, self.key), "event": "download"}

    def bulk_load(self, file_id) -> str:
        """ Load Corporate Number Publication Site data.
        """
        # Download Corporate Number ZIP & Uncompression
        contents = self._download_zip(file_id)
        lines = self._uncompress_file(contents)
        # Convert string objects to List/Dict object
        self.show = self._convert_str_2_csv(lines)
        # Convert blank records to None
        self.show = self._delete_blank(self.show)
        return self.show

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
            raise SystemExit('Request to ' + self.url + ' has been failed: ' + str(res.status_code))
        return res.content

    def _uncompress_file(self, content) -> list:
        # Create Zip Object from response strings
        try:
            zip_object = zipfile.ZipFile(io.BytesIO(content))
        except zipfile.BadZipFile:
            print("Failed to unzip content. The content may not be a valid zip file.")
            raise

        # Uncompress ZIP files & union all files
        # if the Zip file has many text files, the script integrate files to single file.
        lines = []
        for file_name in zip_object.namelist():
            if not re.search(r'.*\.asc', file_name):
                txt = zip_object.open(file_name).read()
                lines += txt.decode().splitlines()
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

    def _delete_blank(self, lines:list) -> list:
        """ Convert blank field ('') to None object
        :param lines: List of dict data
        :return: List object
        """
        for rec in lines:
            for key, val in rec.items():
                rec[key] = None if val == '' else val

        return lines

