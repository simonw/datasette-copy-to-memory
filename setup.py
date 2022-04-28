from setuptools import setup
import os

VERSION = "0.1a0"


def get_long_description():
    with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md"),
        encoding="utf8",
    ) as fp:
        return fp.read()


setup(
    name="datasette-copy-to-memory",
    description="Copy database files into an in-memory database on startup",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Simon Willison",
    url="https://github.com/simonw/datasette-copy-to-memory",
    project_urls={
        "Issues": "https://github.com/simonw/datasette-copy-to-memory/issues",
        "CI": "https://github.com/simonw/datasette-copy-to-memory/actions",
        "Changelog": "https://github.com/simonw/datasette-copy-to-memory/releases",
    },
    license="Apache License, Version 2.0",
    classifiers=[
        "Framework :: Datasette",
        "License :: OSI Approved :: Apache Software License",
    ],
    version=VERSION,
    packages=["datasette_copy_to_memory"],
    entry_points={"datasette": ["copy_to_memory = datasette_copy_to_memory"]},
    install_requires=["datasette"],
    extras_require={"test": ["pytest", "pytest-asyncio", "sqlite-utils"]},
    python_requires=">=3.7",
)
