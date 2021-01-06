# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


setup(
    name="corpus-sampling",
    version="1.0.0",
    description="Corpus sampler",
    long_description="Corpus sampler",
    python_requires=">=3.7.0",
    install_requires=["nltk"],
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        "console_scripts": ["sample-corpus=sampling.sample:parse_cl"]
    },
)
