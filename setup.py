#!/usr/bin/env python3

from pathlib import Path

from setuptools import find_packages, setup

packages = find_packages(exclude=("tests*",))
package_data = {pkg: ("py.typed", "requirements.txt") for pkg in packages}

setup(
    name="languagetool_cli",
    python_requires=">=3.8.0",
    version="0.1.0",
    description="LanguageTool CLI",
    long_description=Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    author="ms-jpq",
    author_email="github@bigly.dog",
    url="https://github.com/ms-jpq/languagetool_cli",
    scripts=("lt-cli",),
    packages=packages,
    package_data=package_data,
)
