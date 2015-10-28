#!/usr/bin/env python

from setuptools import setup
import re
import io
import os.path

dirname = os.path.dirname(os.path.abspath(__file__))
filename = os.path.join(dirname, 'jsonpointer.py')
src = io.open(filename, encoding='utf-8').read()
metadata = dict(re.findall("__([a-z]+)__ = '([^']+)'", src))
docstrings = re.findall('"""(.*)"""', src)

PACKAGE = 'jsonpointer'

MODULES = (
        'jsonpointer',
)

AUTHOR_EMAIL = metadata['author']
VERSION = metadata['version']
WEBSITE = metadata['website']
LICENSE = metadata['license']
DESCRIPTION = docstrings[0]

# Extract name and e-mail ("Firstname Lastname <mail@example.org>")
AUTHOR, EMAIL = re.match(r'(.*) <(.*)>', AUTHOR_EMAIL).groups()

try:
    from pypandoc import convert
    read_md = lambda f: convert(f, 'rst')
except ImportError:
    print('warning: pypandoc module not found, could not convert '
          'Markdown to RST')
    read_md = lambda f: open(f, 'r').read()

CLASSIFIERS = [
    'Development Status :: 5 - Production/Stable',
    'Environment :: Console',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: Implementation :: CPython',
    'Programming Language :: Python :: Implementation :: PyPy',
    'Topic :: Software Development :: Libraries',
    'Topic :: Utilities',
]

setup(name=PACKAGE,
      version=VERSION,
      description=DESCRIPTION,
      long_description=read_md('README.md'),
      author=AUTHOR,
      author_email=EMAIL,
      license=LICENSE,
      url=WEBSITE,
      py_modules=MODULES,
      scripts=['bin/jsonpointer'],
      classifiers=CLASSIFIERS,
)
