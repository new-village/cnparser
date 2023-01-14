# cnparser
**cnparser** is a python library for loading and enrichment [Corporate Number Publication Site](https://www.houjin-bangou.nta.go.jp/en/) data that is provided from National Tax Agency Japan. cnparser only support to parse latest data now.   
  
### Usage
----------------------
To load [netkeiba.com](https://www.netkeiba.com/) data and parse to dictionay file.

#### Basic information (基本3情報)
```python
>>> import cnparser
>>> cndata = cnparser.bulk_load("Shimane")
>>> cndata.show
[{'sequence_number': '1', 'corporate_number': '1000013050246', ... }]
```