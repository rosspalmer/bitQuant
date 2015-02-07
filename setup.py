try:
	from setuptools import setup
except ImportError:
	from distutils.core import setup

config = {
	'description':'bitQuant',
	'author': 'ross palmer',
	'url':'https://github.com/rosspalmer/bitQuant',
	'version': '0.1',
	'install_requires': ['SQLAlchemy','pandas','numpy','scipy'],
	'packages': ['bitquant'],
	'scripts': [],
	'name':'bitquant'
}

setup(**config)
