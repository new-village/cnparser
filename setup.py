''' setup.py
'''
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='cnparser',
    version='$(python -c "import re; version = re.search(rversion='([0-9]+.[0-9]+.[0-9]+), open(setup.py).read()); major, minor, patch = version.group(1).split(.); patch = int(patch) + 1; new_version = f{major}.{minor}.{patch}; print(new_version)")',
    author='new-village',
    url='https://github.com/new-village/cnparser',
    description='cnparser is a parser library of Corporate Number Publication Site data.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license = 'GPLv3+',
    install_requires=['requests', 'bs4', 'pandas', 'pandarallel', 'pykakasi'],
    packages=find_packages(),
    package_data={'': ['config/*.json']},
)
