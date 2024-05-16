# cnparser  
[![Test](https://github.com/new-village/cnparser/actions/workflows/test.yaml/badge.svg)](https://github.com/new-village/cnparser/actions/workflows/test.yaml)  
**cnparser** is a python library for loading and enrichment [Corporate Number Publication Site](https://www.houjin-bangou.nta.go.jp/en/) data that is provided from National Tax Agency Japan. cnparser only support to parse latest data now.   
  
## Installation  
----------------------
cnparser is available on pip installation.
```
$ python -m pip install cnparser
```
  
### GitHub Install
Installing the latest version from GitHub:  
```
$ git clone https://github.com/new-village/cnparser
$ cd cnparser
$ python setup.py install
```
    
## Usage
This section demonstrates how to use this library to load and process data from the National Tax Agency's [Corporate Number Publication Site](https://www.houjin-bangou.nta.go.jp/).

### Direct Data Loading
To load data for a specific prefecture, use the `load` function. By passing the prefecture name as an argument, you can obtain a DataFrame containing data for that prefecture.
To execute the `load` function without specifying any arguments, data for all prefectures across Japan will be loaded. If you wish to load data for a specific prefecture, you must specify the prefecture name in Roman characters ([list of the supported prefecture](https://github.com/new-village/cnparser/blob/main/cnparser/config/file_id.json)) like below: 
```
>>> import cnparser
>>> df = cnparser.load("Shimane")
```

### CSV Data Loading
If you already have a downloaded CSV file, use the `read_csv` function. By passing the file path as an argument, you can obtain a DataFrame with headers from the CSV data.
```
>>> import cnparser
>>> df = cnparser.read_csv("path/to/data.csv")
```

## Tools
### import_dict.py: Bilingual Emacspeak Project (BEP) Dictionary Import Tool
This tool imports the [BEP dictionary](https://fastapi.metacpan.org/source/MASH/Lingua-JA-Yomi-0.01/lib/Lingua/JA) and generates a dictionary file for use with cnparser. It processes the bilingual mappings from English to Kana, ensuring that cnparser can accurately handle and transform data involving these language elements.
```
$ cd /home/<USER>/analysis
$ python enrich.py <FILE_PATH>
```
