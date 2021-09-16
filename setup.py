#!/usr/bin/env python

from setuptools import find_packages, setup

from arnold import __version__ as version


try:
    with open("requirements.txt", "r") as f:
        install_requires = [x.strip() for x in f.readlines()]
except IOError:
    install_requires = []

with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name="ARNOLD",
    version=version,
    description="Clinical Genomics Core database and REST api",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Maya Brandi",
    url="https://github.com/Clinical-Genomics/ARNOLD",
    author_email="maya.brandi@scilifelab.se",
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        "console_scripts": ["arnold=arnold.commands:cli"],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
