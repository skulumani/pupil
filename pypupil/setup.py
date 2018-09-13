"""Setup tools based creation for pupil package using cython
"""
from __future__ import absolute_import, division, print_function, unicode_literals

try:
    # Python 3
    MyFileNotFoundError = FileNotFoundError
except:  # FileNotFoundError does not exist in Python 2.7
    # Python 2.7
    # - open() raises IOError
    # - remove() (not currently used here) raises OSError
    MyFileNotFoundError = (IOError, OSError)

libname = "pupil"
build_type = "optimized"

SHORTDESC = "Pupil package extracted from pupil labs"

DESC = """Pupil package from pupil labs

Tested on Python 3.6
"""

# Directories (relative to the top-level directory where setup.py resides) in which to look for data files.
datadirs  = ("test",)

# File extensions to be considered as data files. (Literal, no wildcards.)
dataexts  = (".py",  ".pyx", ".pxd",  ".c", ".cpp", ".h",  ".sh",  ".lyx", ".tex", ".txt", ".pdf")

# Standard documentation to detect (and package if it exists).
#
standard_docs     = ["README", "LICENSE", "TODO", "CHANGELOG", "AUTHORS"]  # just the basename without file extension
standard_doc_exts = [".md", ".rst", ".txt", ""]  # commonly .md for GitHub projects, but other projects may use .rst or .txt (or even blank).

#########################################################
# Init
#########################################################

# check for Python 2.7 or later
# http://stackoverflow.com/questions/19534896/enforcing-python-version-in-setup-py
import sys
if sys.version_info < (2,7):
    sys.exit('Sorry, Python < 2.7 is not supported')

import os

from setuptools import setup
from setuptools.extension import Extension

try:
    from Cython.Build import cythonize
except ImportError:
    sys.exit("Cython not found. Cython is needed to build the extension modules.")

try:
    import numpy as np
except ImportError:
    sys.exit("Numpy not found. Numpy is required to build the module")


