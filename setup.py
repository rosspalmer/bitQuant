try:
	from setuptools import setup
except ImportError:
	from distutils.core import setup

config = {
	'description':'bitQuant',
	'author': 'ross palmer',
	'url':'https://github.com/rosspalmer/bitQuant',
	'license':'MIT',
	'version': '0.2.6',
	'install_requires': ['SQLAlchemy','pandas','numpy','scipy','PyMySQL'],
	'packages': ['bitquant'],
	'scripts': [],
	'name':'bitquant'
}

setup(**config)
