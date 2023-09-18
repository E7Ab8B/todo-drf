# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# Path setup
# ------------------------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.

import os
import sys

import django

if os.getenv('READTHEDOCS') in ('True', 'true', 1, '1'):
    sys.path.insert(0, os.path.abspath('..'))
    os.environ['DJANGO_READ_DOT_ENV_FILE'] = 'True'
    os.environ['USE_DOCKER'] = 'no'
else:
    sys.path.insert(0, os.path.abspath('/app'))

os.environ['DATABASE_URL'] = 'sqlite:///readthedocs.db'
os.environ['CELERY_BROKER_URL'] = os.getenv('CELERY_BROKER_URL', 'amqp://guest:guest@rabbitmq:5672/')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

# Project information
# ------------------------------------------------------------------------------

project = "ToDo"
copyright = """2023, ToDo"""  # pylint: disable=redefined-builtin

# General configuration
# ------------------------------------------------------------------------------

# https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-extensions
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
    # Third Party Extensions
    # https://sphinxcontrib-django.readthedocs.io/en/latest/index.html
    'sphinxcontrib_django',
    'sphinx.ext.autosectionlabel',
]


# https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-exclude_patterns
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html#confval-autoclass_content
autoclass_content = 'both'

# HTML configuration
# ------------------------------------------------------------------------------

# https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-html_theme
html_theme = 'alabaster'

# sphinxcontrib-django
# ------------------------------------------------------------------------------

# https://sphinxcontrib-django.readthedocs.io/en/latest/readme.html#configuration
django_settings = os.getenv('DJANGO_SETTINGS_MODULE')
django_show_db_tables = True
