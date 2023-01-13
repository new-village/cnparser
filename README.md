# cnparser
**cnparser** is a python library for loading and enrichment [Corporate Number Publication Site](https://www.houjin-bangou.nta.go.jp/en/) data that is provided from National Tax Agency Japan. cnparser only support to parse latest data now.   
  
### Usage
----------------------
To load [netkeiba.com](https://www.netkeiba.com/) data and parse to dictionay file.

#### Basic information (基本3情報)
```python
>>> import cnparser
>>> cndata = cnparser.load("tottori")
>>> cndata.info
[{'corp_number': '1000013050238', 'corp_name': '鳥取簡易裁判所', 'corp_kana': 'トットリカンイサイバンショ', ... }]
```