## Overview

Library authored by Tom Arn (sw@tanapro.ch) with additional functionality
for the Beeware Toga framework (beeware.org)

## Dependencies

The library has following dependencies:

1. briefcase
2. Toga
3. python-i18n[YAML]

To create the docs, following packages are needed (see sphinx-setup.txt):`sphinx`

For formatting the code: `black`

## How to setup the venv

Use Python 3.11 - higher versions might not work with Chaquopy yet
```bash
cd taTogaLib
py -m venv .venv
.venv\Scripts\activate
pip install python-i18n[YAML] briefcase sphinx black
pip install -e c:\Projects\Python\Toga\core
pip install -e c:\Projects\Python\Toga\winforms
```
## How to run an example (e.g. for the window module) on Windows

From the venv:
```bash
cd examples\ui\window
briefcase dev -r
```

## How to run an example (e.g. for the window module) on Android

From the venv:
```bash
cd examples\ui\window
test-android.bat
```
## How to create the docs

1. Set the release date in docs/conf.py
1. Add new modules to docs/source/index.rst (automodule lines)
1. `cd docs`
1. `make clean`
1. `make html` or `make singlehtml`