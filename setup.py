#!/usr/bin/env python
# -*- coding: utf-8 -*

import os
import pathlib

from setuptools import find_packages, setup

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

REPO_ROOT = pathlib.Path(__file__).parent

# Fetch the long description from the readme
with open(REPO_ROOT / "README.md", encoding="utf-8") as f:
    README = f.read()

install_requires = (
    'google-generativeai',
    'click',
    'attrs',
    )

setup(
    name="phil-docstring",
    version=1,
    include_package_data=True,
    description="Tool for adding doc strings to python files using an LLM.",
    long_description=README,
    long_description_content_type="text/markdown",  
    author="Joe Sharman",
    package_dir={"": "src"},
    packages=find_packages("src"),
    install_requires=install_requires,
    process_dependency_links=True,
    entry_points={
        'console_scripts': [
            'phil = phil_docstrings.interface:run',
        ],
    },
)
