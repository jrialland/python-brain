#!/usr/bin/env python
from setuptools import setup
import brain

setup(
    name='pythonbrain',
        version=brain.__version__,
        author=brain.__author__,
        author_email=brain.__email__,
        url='http://github.com/jrialland/python-brain',
        download_url='https://github.com/jrialland/python-brain/tarball/' +
            str(brain.__version__),
        packages=['brain'],
        description='lightweight neural network library for Python',
        provides=['brain'],
        long_description='lightweight neural network library for Python',
        zip_safe=True,
        license=brain.__license__,
        include_package_data=True,
        keywords=['ia', 'neural network'],
        classifiers=[
                'Intended Audience :: Developers',
                'Operating System :: OS Independent',
                'Topic :: Software Development',
                'Programming Language :: Python',
        ]
)
