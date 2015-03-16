#!/usr/bin/env python2.7

classifiers = [
    "Development Status :: 5 - Production/Stable",
    "Environment :: Console",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: Apache Software License",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 2.7",
    "Topic :: Software Development :: Code Generators",
    "Topic :: Software Development :: Libraries :: Python Modules",
]

from distutils.core import setup

setup(
    name="3to2",
    packages=["lib3to2", "lib3to2.fixes", "lib3to2.tests"],
    scripts=["3to2"],
    version="1.0",
    url="http://www.startcodon.com/wordpress/?cat=8",
    author="Joe Amenta",
    author_email="amentajo@msu.edu",
    classifiers=classifiers,
    description="Refactors valid 3.x syntax into valid 2.x syntax, if a syntactical conversion is possible",
    long_description="",
    license="",
    platforms="",
)
