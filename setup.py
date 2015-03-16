try:
	from setuptools import setup
except ImportError:
	from distutils.core import setup

config = {
	'description':'End to end solution for bitcoin data gathering, backtesting, and live trading',
	'author': 'ross palmer',
	'url':'http://rosspalmer.github.io/bitQuant/',
	'license':'MIT',
	'version': '0.2.9',
	'install_requires': ['SQLAlchemy','pandas','numpy','scipy','PyMySQL'],
	'packages': ['bitquant'],
	'scripts': [],
	'name':'bitquant'
}

setup(**config)
