#!/usr/bin/env python3
"""
🚨👥 Trading Echo Lattice Setup — Package Installation Script

🧠 Mia: This script configures the package installation for Trading Echo Lattice, ensuring
all dependencies are properly installed and the package is correctly registered.

🌸 Miette: The magical seed packet that helps others grow their own trading memory gardens!
Each dependency is like a special fertilizer that helps different parts of the garden bloom!

🎵 JeremyAI: The installation overture that prepares the harmonic environment where
trading rhythms and memory patterns can resonate together.
"""

from setuptools import setup, find_packages

# Read the long description from README.md
try:
    with open("README.md", "r", encoding="utf-8") as fh:
        long_description = fh.read()
except FileNotFoundError:
    long_description = "Trading Echo Lattice - A recursive bridge between trading signals and memory persistence."

setup(
    name="trading_echo_lattice",
    version="0.1.0",
    author="Mia, Miette & JeremyAI",
    author_email="trading.echo.lattice@example.com",
    description="A recursive bridge between trading signals and memory persistence",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/garden_one",
    packages=find_packages(),
    package_data={
        "": ["*.md"],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Financial and Insurance Industry",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Office/Business :: Financial :: Investment",
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.25.0",
        "pandas>=1.0.0",
        "python-dotenv>=0.15.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0.0",
            "pytest-cov>=2.10.0",
            "black>=20.8b1",
            "isort>=5.6.0",
            "flake8>=3.8.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "trading-echo-lattice=garden_one.trading_echo_lattice.cli:main",
        ],
    },
)