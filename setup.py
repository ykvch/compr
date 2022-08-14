from setuptools import setup
from pathlib import Path

__version__ = "0.1.4"

NAME = "compr"
CLASSIFIERS = [
    "Programming Language :: Python",
]

PROJECT_URLS = {
    "Bug Tracker": "https://github.com/ykvch/compr/issues",
    "Source Code": "https://github.com/ykvch/compr",
}

LONG_DESCRIPTION = (Path(__file__).parent / "README.md").read_text()

setup(
    name=NAME,
    version=__version__,
    description='Handy wrappers for advanced object comparing and matching.',
    package_dir={"": "src"},
    project_urls=PROJECT_URLS,
    classifiers=CLASSIFIERS,
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
)
