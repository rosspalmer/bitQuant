try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description':'Bitcoin trade and exchange data miner',
    'author': 'ross palmer',
    'url':'http://rosspalmer.github.io/bitQuant/',
    'license':'MIT',
    'version': '0.3.0',
    'install_requires': ['SQLAlchemy','pandas','numpy','scipy','PyMySQL'],
    'packages': ['bitquant'],
    'scripts': [],
    'name':'bitquant'
}

setup(**config)
