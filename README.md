## Overview

Library authored by Tom Arn (sw@tanapro.ch) with additional functionality 
for the Beeware Toga framework (beeware.org)

## Dependencies

The library has following dependencies:

1. briefcase
1. Toga
1. python-i18n[YAML]

To create the docs, following packages are needed (see sphinx-setup.txt):

1. sphinx

For formatting the code:

1. black


## How to setup the venv

Use Python 3.9 - higher versions might not work with Chaquopy yet

1. cd taTogaLib
1. py -m venv .venv
1. .venv\Scripts\activate
1. pip install python-i18n[YAML]
1. pip install briefcase
1. pip install -e c:\Projects\Python\Toga\core
1. pip install -e c:\Projects\Python\Toga\winforms
1. pip install sphinx
1. pip install black


## How to run an example (e.g. for the window module) on Windows

From the venv:
1. cd examples\ui\window
1. briefcase dev -r


## How to run an example (e.g. for the window module) on Android

From the venv:
1. cd examples\ui\window
1. test-android.bat


## How to create the docs

1. Set the release date in docs/conf.py
1. Add new modules to docs/source/index.rst (automodule lines)
1. cd docs
1. make clean
1. make html

or: make singlehtml