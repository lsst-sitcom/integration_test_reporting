#!/usr/bin/env python
import os.path
from setuptools import setup

version = "0.1.0"
with open("./python/lsst/integration_test_reporting/version.py", "w") as f:
    print(f"""
__all__ = ("__version__", )
__version__='{version}'""", file=f)

# read the contents of your README file
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, "README.md"), encoding='utf-8') as f:
    long_description = f.read()

install_requirements = None
with open('requirements/install.txt') as installFile:
    requirements = [x.strip() for x in installFile]

test_requirements = None
with open('requirements/test.txt') as testFile:
    test_requirements = [x.strip() for x in testFile if not x.startswith('-')]

setup(
    version=f"{version}",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=install_requirements,
    tests_require=test_requirements
)
