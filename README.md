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
----------------------
Many properties are available once the cnparser object is created.  
  
### Collect basic information (基本3情報)
```python
>>> import cnparser
>>> cndata = cnparser.bulk_load("Shimane")
>>> print(cndata)
[{'sequence_number': '1', 'corporate_number': '1000013050246', ...,  'hihyoji': '0'}, {...}]
```

### Import basic information (基本3情報)
If you have an unzipped basic information (基本3情報), you can load file this library.
```python
>>> import cnparser
>>> cndata = cnparser.read_csv_file("path/to/data.csv")
>>> print(cndata)
[{'sequence_number': '1', 'corporate_number': '1000013050246', ...,  'hihyoji': '0'}, {...}]
```

### `enrich_kana` function
The `enrich_kana` function takes a list of corporate information and generates Kana (furigana) for each company name, returning the results as a list. This function processes through multiple steps including normalization of the company name, removal of corporate form suffixes, and conversion to Katakana.

```python
>>> import cnparser
>>> enriched = cnparser.enrich_kana(cndata)
>>> print(enriched)
[{'sequence_number': '1', 'name': '山田商事株式会社', ...,  'e_furigana': 'ヤマダショウジ'}, {...}]
```

  
### Enrich information from `bulk_load` result
```python
>>> import cnparser
>>> enriched = cnparser.bulk_enrich(cndata)
>>> print(enriched)
[{'sequence_number': '1', ..., 'lat': 34.978982, 'lng': 132.525163, 'level': 3}, {...}]
```

### Enrich information from downloaded CSV File
```python
>>> import cnparser
>>> enriched = cnparser.bulk_enrich("path/to/data.csv")
>>> print(enriched)
[{'sequence_number': '1', ..., 'lat': 34.978982, 'lng': 132.525163, 'level': 3}, {...}]
```

### Enrich information to CSV file  
You can export enriched data to CSV file directry by `export_file` option with file name.
```python
>>> import cnparser
>>> enriched = cnparser.bulk_enrich(cndata, export_file="path/to/export/data.csv")
```

### Enrich information to CSV file with downloaded api
If you enrich massive data, You can use downloaded api.
```
$ cd /home/<USER>/
$ curl -sL https://github.com/geolonia/japanese-addresses/archive/refs/heads/master.tar.gz | tar xvfz -
```

```python
>>> import cnparser
>>> enriched = cnparser.bulk_enrich(cndata, api_path="file:///home/<USER>/japanese-addresses-master/api/ja")
```

## Tools
### import_dict.py: Bilingual Emacspeak Project (BEP) Dictionary Import Tool
This tool imports the [BEP dictionary](https://fastapi.metacpan.org/source/MASH/Lingua-JA-Yomi-0.01/lib/Lingua/JA) and generates a dictionary file for use with cnparser. It processes the bilingual mappings from English to Kana, ensuring that cnparser can accurately handle and transform data involving these language elements.
```
$ cd /home/<USER>/analysis
$ python enrich.py <FILE_PATH>
```
