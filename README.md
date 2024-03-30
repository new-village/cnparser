# cnparser  
[![Test](https://github.com/new-village/cnparser/actions/workflows/test.yaml/badge.svg)](https://github.com/new-village/cnparser/actions/workflows/test.yaml)  
**cnparser** is a python library for loading and enrichment [Corporate Number Publication Site](https://www.houjin-bangou.nta.go.jp/en/) data that is provided from National Tax Agency Japan. cnparser only support to parse latest data now.   
  
### Installation  
----------------------
cnparser is available on pip installation.
```
$ python -m pip install cnparser
```
  
#### GitHub Install
Installing the latest version from GitHub:  
```
$ git clone https://github.com/new-village/cnparser
$ cd cnparser
$ python setup.py install
```
    
### Usage
----------------------
Many properties are available once the cnparser object is created.  
  
#### Collect basic information (基本3情報)
```python
>>> import cnparser
>>> cndata = cnparser.bulk_load("Shimane")
>>> print(cndata)
[{'sequence_number': '1', 'corporate_number': '1000013050246', ...,  'hihyoji': '0'}, {...}]
```
  
#### Enrich information from `bulk_load` result
```python
>>> import cnparser
>>> enriched = cnparser.bulk_enrich(cndata)
>>> print(enriched)
[{'sequence_number': '1', ..., 'lat': 34.978982, 'lng': 132.525163, 'level': 3}, {...}]
```

#### Enrich information from downloaded CSV File
```python
>>> import cnparser
>>> enriched = cnparser.bulk_enrich("path/to/data.csv")
>>> print(enriched)
[{'sequence_number': '1', ..., 'lat': 34.978982, 'lng': 132.525163, 'level': 3}, {...}]
```

#### Enrich information to CSV file  
You can export enriched data to CSV file directry by `export_file` option with file name.
```python
>>> import cnparser
>>> enriched = cnparser.bulk_enrich(cndata, export_file="path/to/export/data.csv")
```
