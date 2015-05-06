try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

config = {
    'description':'Bitcoin trade and exchange data miner',
    'author': 'ross palmer',
    'url':'http://rosspalmer.github.io/bitQuant/',
    'license':'MIT',
    'version': '0.3.1',
    'install_requires': ['SQLAlchemy','pandas','numpy','PyMySQL'],
    'packages': find_packages(),
    'scripts': [],
    'name':'bitquant'
}

setup(**config)
