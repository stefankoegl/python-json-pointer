# Sphinx configuration for the python-json-pointer documentation.
# See https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys

# Document the jsonpointer module from this checkout
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

import jsonpointer  # noqa: E402

# -- Project information -------------------------------------------------------

project = 'python-json-pointer'
author = 'Stefan Kögl'
copyright = jsonpointer.__author__
version = jsonpointer.__version__
release = jsonpointer.__version__

# -- General configuration -----------------------------------------------------

extensions = ['sphinx.ext.autodoc']
exclude_patterns = ['_build']
pygments_style = 'sphinx'

# -- Options for HTML output ---------------------------------------------------

html_theme = 'classic'
htmlhelp_basename = 'python-json-pointerdoc'

# -- Options for other output formats ------------------------------------------

latex_documents = [
    ('index', 'python-json-pointer.tex', 'python-json-pointer Documentation',
     author, 'manual'),
]

man_pages = [
    ('index', 'python-json-pointer', 'python-json-pointer Documentation',
     [author], 1),
]

texinfo_documents = [
    ('index', 'python-json-pointer', 'python-json-pointer Documentation',
     author, 'python-json-pointer', jsonpointer.__doc__.strip(),
     'Miscellaneous'),
]
