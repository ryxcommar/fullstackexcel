from setuptools import setup

setup(
    name='fullstackexcel',
    version='0.0.1',
    py_modules=['fullstackexcel'],
    author='@ryxcommar',
    url='https://twitter.com/ryxcommar',
    entry_points={
        'console_scripts': ['fullstackexcel=fullstackexcel:cli']
    },
    install_requires=['flask', 'pandas', 'xlrd', 'xlsxwriter']
)
