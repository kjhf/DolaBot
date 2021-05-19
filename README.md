# Dola
Dola is a Python-based bot specialising in Splatoon and [Slapp](https://github.com/kjhf/SplatTag) but also comes with some utility functions.
Code on [Github](https://github.com/kjhf/DolaBot).

Import prefix is `DolaBot`.

## Requirements
- Python 3.9+

## Distribution
The following commands should be entered into the venv console:

Windows:

    rmdir /S build
    rmdir /S dist
    py -m pip install --upgrade build
    py -m build
    py -m pip install --upgrade twine
    py -m twine upload dist/*

Linux:

    rm -r build
    rm -r dist
    python3 -m pip install --upgrade build
    python3 -m build
    python3 -m pip install --upgrade twine
    python3 -m twine upload dist/*
