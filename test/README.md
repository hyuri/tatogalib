## Overview

Test applications for tatogalib

## Dependencies

This application has following dependencies:

1. briefcase
1. Toga
1. python-i18n[YAML]

## How to setup the testing venv

Use Python 3.9 - higher versions might not work with Chaquopy yet

1. cd taTogaLib\test
1. py -m venv .venv
1. .venv\Scripts\activate
1. pip install python-i18n[YAML]
1. pip install briefcase
1. pip install -e c:\Projects\Python\Toga\core
1. pip install -e c:\Projects\Python\Toga\winforms


## How to run a test (e.g. for the window module)

From the testing venv:
1. cd test\ui\window
1. briefcase dev -r
