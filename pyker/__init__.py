# -*- coding: utf-8 -*-
"""
Pyker
=====

Pythonic library to ease the use of
`expandvr API<https://github.com/tooxie/pyconuy>`_.
"""
from .recognizer import GenderRecognizer
from .exceptions import (
    UnsupportedFormatError, ServerError, InsufficientDataError,
    FileDoesNotExistError, ConversionError)

__all__ = [
    FileDoesNotExistError,
    GenderRecognizer,
    InsufficientDataError,
    ServerError,
    UnsupportedFormatError,
    ConversionError,
]
__version__ = '0.0.1'
__author__ = u'Alvaro Mouriño'
__author_email__ = 'alvaro@mourino.net'
