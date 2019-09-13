# ZFuzz documentation build configuration file

import os
import sys

sys.path.insert(0, os.path.abspath('../'))

import zfuzz


project = 'ZFuzz'
copyright = '2019, Zepp'
author = 'Zepp'
release = '1.2'

master_doc = 'index'

extensions = ['sphinx.ext.autodoc', 'sphinx_rtd_theme']

html_theme = 'sphinx_rtd_theme'
