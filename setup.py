from setuptools import setup, find_packages

setup(
    name="karten",
    version="0.0.2",
    packages=find_packages(),
    install_requires=["click", "google-generativeai"],
    entry_points={
        "console_scripts": [
            "karten=karten.cli:cli",
        ],
    },
)
