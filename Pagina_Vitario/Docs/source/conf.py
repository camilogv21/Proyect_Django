# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys

sys.path.insert(0, os.path.abspath('../../'))


project = 'Vitario'
copyright = '2022, Juan Camilo Galeano Velez'
author = 'Juan Camilo Galeano Velez'
release = '2.7.18'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.autodoc',
        'sphinx.ext.todo',
        'sphinx.ext.autosummary',
        'sphinx.ext.viewcode'
]

templates_path = ['_templates']
exclude_patterns = []

root_doc = 'index'
language = 'es'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'nature'
html_static_path = ['_static']

html_sidebars = { '**': ['globaltoc.html', 'relations.html',
        'sourcelink.html', 'searchbox.html'], }
