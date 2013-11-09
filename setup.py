#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

import pyker

setup(
    name='pyker',
    version=pyker.__version__,
    description='Expand voice recognition library',
    long_description=pyker.__doc__,
    author=pyker.__author__,
    author_email=pyker.__author_email__,
    url='https://github.com/expanduc/pyconuy',
    license='MIT',
    platforms=['OS-independent', 'Any'],
    package_dir={'': '.'},
    packages=find_packages('.'),
    install_requires=[
        'requests==2.0.1',
    ],
)
