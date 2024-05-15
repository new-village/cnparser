import requests
import json
import re
import os
from bs4 import BeautifulSoup

def fetch_webpage(url):
    """
    Fetches the HTML content of a webpage given a URL.
    
    Args:
    url (str): The URL of the webpage to fetch.
    
    Returns:
    BeautifulSoup: A BeautifulSoup object containing the parsed HTML of the webpage.
    """
    response = requests.get(url)
    return BeautifulSoup(response.text, 'html.parser')

def extract_file_ids(soup, pref):
    """
    Extracts file IDs from the parsed HTML of a webpage.
    
    Args:
    soup (BeautifulSoup): The BeautifulSoup object containing the parsed HTML.
    pref (dict): A dictionary mapping Japanese prefecture names to English.
    
    Returns:
    dict: A dictionary mapping region names to their corresponding file IDs.
    """
    unicode_table = soup.find('div', class_='inBox21').find_all('div', class_='tbl02')[1]
    rows = unicode_table.find_all('dl')
    region_file_ids = {}
    for row in rows:
        region_name_jp = row.find('dt', class_='mb05').text.strip()
        region_name = pref.get(region_name_jp, region_name_jp)  # Convert Japanese to English if possible
        file_id = re.search(r'\d{5}', row.find('a').get('onclick')).group()  # Extract file ID using regex
        region_file_ids[region_name] = file_id
    return region_file_ids

def save_file_ids(region_file_ids):
    """
    Saves the extracted file IDs to a JSON file.
    
    Args:
    region_file_ids (dict): A dictionary containing region names and their corresponding file IDs.
    """
    file_path = os.path.join(os.path.dirname(__file__), '../cnparser/config/file_id.json')
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(region_file_ids, file, ensure_ascii=False, indent=4)

url = "https://www.houjin-bangou.nta.go.jp/download/zenken/"

# Dictionary mapping Japanese prefecture names to English
pref = {
    "全国": "All",
    "北海道": "Hokkaido",
    "青森県": "Aomori",
    "岩手県": "Iwate",
    "宮城県": "Miyagi",
    "秋田県": "Akita",
    "山形県": "Yamagata",
    "福島県": "Fukushima",
    "茨城県": "Ibaraki",
    "栃木県": "Tochigi",
    "群馬県": "Gunma",
    "埼玉県": "Saitama",
    "千葉県": "Chiba",
    "東京都": "Tokyo",
    "神奈川県": "Kanagawa",
    "新潟県": "Niigata",
    "富山県": "Toyama",
    "石川県": "Ishikawa",
    "福井県": "Fukui",
    "山梨県": "Yamanashi",
    "長野県": "Nagano",
    "岐阜県": "Gifu",
    "静岡県": "Shizuoka",
    "愛知県": "Aichi",
    "三重県": "Mie",
    "滋賀県": "Shiga",
    "京都府": "Kyoto",
    "大阪府": "Osaka",
    "兵庫県": "Hyogo",
    "奈良県": "Nara",
    "和歌山県": "Wakayama",
    "鳥取県": "Tottori",
    "島根県": "Shimane",
    "岡山県": "Okayama",
    "広島県": "Hiroshima",
    "山口県": "Yamaguchi",
    "徳島県": "Tokushima",
    "香川県": "Kagawa",
    "愛媛県": "Ehime",
    "高知県": "Kochi",
    "福岡県": "Fukuoka",
    "佐賀県": "Saga",
    "長崎県": "Nagasaki",
    "熊本県": "Kumamoto",
    "大分県": "Oita",
    "宮崎県": "Miyazaki",
    "鹿児島県": "Kagoshima",
    "沖縄県": "Okinawa",
    "国外": "Other"
}

if __name__ == "__main__":
    soup = fetch_webpage(url)
    region_file_ids = extract_file_ids(soup, pref)
    save_file_ids(region_file_ids)
