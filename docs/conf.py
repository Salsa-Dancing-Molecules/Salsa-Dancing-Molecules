# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys
sys.path.insert(0, os.path.abspath('../'))

project = 'Salsa Dancing Molecules'
copyright = '2022, Salsa Dancing Molecules project members'
author = 'Salsa Dancing Molecules project members'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
            'sphinx.ext.duration',
            'sphinx.ext.doctest',
            'sphinx.ext.autodoc',
            'sphinx.ext.autosummary',
            'sphinx.ext.intersphinx',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

autosummary_generate = True
autoclass_content = 'both'
set_type_checking_flag = True

html_theme = "default"

html_theme_options = {
    "navigation_depth": 4
}

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_static_path = ['_static']
