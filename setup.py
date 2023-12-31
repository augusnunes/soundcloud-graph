#!/usr/bin/env python

from distutils.core import setup


def readme():
    with open('README.md', encoding="UTF-8") as f:
        return f.read()

setup(
    name="soundcloud-graph",
    version="0.1.0",
    description="",
    long_description=readme(),
    long_description_content_type='text/markdown',
    author="augusnunes",
    author_email="nunes.augusto19@gmail.com",
    url="https://github.com/augusnunes/soundcloud-graph",
    packages=["soundcloudgraph"],
    install_requires=[
        "scdl>=2.7.3",
        "numpy>=1.26.2",
        "pandas>=2.1.3",
    ],
    extras_require={
        "test": ["coveralls", "pytest", "pytest-dotenv"]
    },
    classifiers=[
        # "Programming Language :: Python :: 3.6",
        # "Programming Language :: Python :: 3.7",
        # "Programming Language :: Python :: 3.8",
        # "Programming Language :: Python :: 3.9",
        # "License :: OSI Approved :: MIT License",
        # "Operating System :: OS Independent"
    ],
    python_requires = ">=3.10",
    project_urls={
        # "Bug Tracker": "https://github.com/7x11x13/soundcloud.py/issues"
    }
)