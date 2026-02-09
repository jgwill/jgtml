#!/usr/bin/env Python
"""
jgtml
"""

from setuptools import find_packages, setup
import re
from pathlib import Path

def read_version():
    """Read version from __init__.py without importing."""
    init_file = Path(__file__).parent / "jgtml" / "__init__.py"
    if not init_file.exists():
        return "0.0.0"
    content = init_file.read_text()
    match = re.search(r'version\s*=\s*["\']([^"\']+)["\']', content)
    if match:
        return match.group(1)
    return "0.0.0"

version = read_version()
        # for line in f:
        #     #print(line)
        #     if line.startswith("version="):
        #         version_match = re.search(r"version=['\"]([^'\"]*)['\"]", line)
        #         return version_match
                #return line.strip().split()[-1][1:-1]

version = read_version()

#print(f"Version: {version}")
setup(
    name="jgtml",
    version=version,
    description="JGTrading Data maker' Dataframes",
    long_description=open("README.rst").read(),
    author="GUillaume Isabelle",
    author_email="jgi@jgwill.com",
    url="https://github.com/jgwill/jgtml",
    packages=find_packages(include=["jgtml"], exclude=["*test*"]),

    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Financial and Insurance Industry",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3.7.16",
    ],
)
