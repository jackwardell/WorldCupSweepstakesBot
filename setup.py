from pathlib import Path

from setuptools import find_packages
from setuptools import setup

__version__ = "0.1.0"
ROOT_DIR = Path(".")

setup(
    name="src",
    version=__version__,
    packages=find_packages(),
    include_package_data=True,
    author="Jack Wardell",
    author_email="jack@wardell.xyz",
    url="https://github.com/JackWardell/",
    description="Bot",
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Natural Language :: English",
        "Intended Audience :: Developers",
    ],
    keywords="python",
    python_requires=">=3.8",
)
