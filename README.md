# cnparser
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
>>> cndata.show
[{'sequence_number': '1', 'corporate_number': '1000013050246', ... }]
```