''' setup.py
'''
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='cnparser',
    version='1.0.0',
    author='new-village',
    url='https://github.com/new-village/cnparser',
    description='cnparser is a parser library of Corporate Number Publication Site data.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license = 'Apache License 2.0',
    install_requires=['requests', 'bs4', 'kanjize==1.2.0', 'normalize-japanese-addresses==0.0.5'],
    packages=find_packages(),
    package_data={'': ['config/*.json']},
)
