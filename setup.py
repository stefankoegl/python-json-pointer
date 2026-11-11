#!/usr/bin/env python

import os.path
import re

from setuptools import setup

dirname = os.path.dirname(os.path.abspath(__file__))
filename = os.path.join(dirname, 'jsonpointer.py')
with open(filename, encoding='utf-8') as f:
    src = f.read()
metadata = dict(re.findall("__([a-z]+)__ = '([^']+)'", src))
docstrings = re.findall('"""(.*)"""', src)

PACKAGE = 'jsonpointer'

MODULES = (
    'jsonpointer',
)

AUTHOR_EMAIL = metadata['author']
VERSION = metadata['version']
WEBSITE = metadata['website']
DESCRIPTION = docstrings[0]

# Extract name and e-mail ("Firstname Lastname <mail@example.org>")
AUTHOR, EMAIL = re.match(r'(.*) <(.*)>', AUTHOR_EMAIL).groups()

with open(os.path.join(dirname, 'README.md'), encoding='utf-8') as readme:
    long_description = readme.read()

CLASSIFIERS = [
    'Development Status :: 5 - Production/Stable',
    'Environment :: Console',
    'Intended Audience :: Developers',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.10',
    'Programming Language :: Python :: 3.11',
    'Programming Language :: Python :: 3.12',
    'Programming Language :: Python :: 3.13',
    'Programming Language :: Python :: 3.14',
    'Programming Language :: Python :: 3.15',
    'Programming Language :: Python :: Implementation :: CPython',
    'Programming Language :: Python :: Implementation :: PyPy',
    'Topic :: Software Development :: Libraries',
    'Topic :: Utilities',
    'Typing :: Typed',
]

setup(
    name=PACKAGE,
    version=VERSION,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=AUTHOR,
    author_email=EMAIL,
    license_expression='BSD-3-Clause',
    url=WEBSITE,
    py_modules=MODULES,
    # PEP 561 stub-only package, shipped in the same distribution
    packages=['jsonpointer-stubs'],
    package_data={'jsonpointer-stubs': ['__init__.pyi']},
    scripts=['bin/jsonpointer'],
    classifiers=CLASSIFIERS,
    python_requires='>=3.10',
)
