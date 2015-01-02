#!/usr/bin/env python
from setuptools import setup

setup(
	name='brain',
	version='0.1',
	author='Julien Rialland',
	author_email='julien.rialland@gmail.com',
	url='http://github.com/jrialland/python-brain',
	download_url = 'https://github.com/jrialland/python-brain/tarball/0.1',
        packages='brain',
	description='lightweight neural network library for Python',
	provides=['brain'],
	long_description='lightweight neural network library for Python',
	zip_safe=True,
	license='BSD',
	include_package_data=True,
	keywords=['ia','neural network'],
	classifiers=[
		'Intended Audience :: Developers',
		'Operating System :: OS Independent',
		'Topic :: Software Development',
		'Programming Language :: Python',
	]
)
