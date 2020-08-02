import re
from setuptools import setup


with open('README.md', 'r', encoding='utf8') as f:
    readme = f.read()


with open('fullstackexcel/_version.py', 'r', encoding='utf8') as f:
    version = re.match("VERSION = '(.*?)'", f.read())[1]


setup(
    name='fullstackexcel',
    version=version,
    py_modules=['fullstackexcel'],
    author='@ryxcommar',
    maintainer='@ryxcommar',
    url='https://twitter.com/ryxcommar',
    entry_points={
        'console_scripts': ['fse=fullstackexcel:cli']
    },
    install_requires=['flask', 'pandas', 'xlrd', 'xlsxwriter'],
    long_description=readme,
    python_requires='>=3.6'
)
