# -*- coding: utf-8 -*-
from nose import tools as nose
from os import path
import mock
import unittest

from pyker import (GenderRecognizer, UnsupportedFormatError,
                  FileDoesNotExistError)

from .mocks import requests_mock

# Test: <sync | async>, <male | female>, <online | mocked>, <valid | invalid>,
# <convert | dont_convert>, <es | de>


class GenderRecognizerTests(unittest.TestCase):
    def setUp(self):
        cwd = path.dirname(__file__)
        # Thanks to https://www.youtube.com/watch?v=_mREmb17KW8
        self.mp3_15s_es = path.join(cwd, 'source-15s-es.mp3')
        self.wav_15s_es = path.join(cwd, 'source-15s-es.wav')

    @mock.patch('requests.post', new=requests_mock)
    def test_correct_format_audio(self, *args, **kwargs):
        genrec = GenderRecognizer(self.wav_15s_es)
        result = genrec.recognize(async=False)

        nose.eq_(result, GenderRecognizer.FEMALE)
        nose.eq_(genrec.is_female(), True)

    @mock.patch('requests.post', new=requests_mock)
    def test_audio_as_file(self, *args, **kwargs):
        genrec = GenderRecognizer(open(self.wav_15s_es, 'rb'))
        result = genrec.recognize(async=False)

        nose.eq_(result, GenderRecognizer.FEMALE)
        nose.eq_(genrec.is_female(), True)

    @nose.raises(UnsupportedFormatError)
    def test_unsupported_format(self):
        genrec = GenderRecognizer(self.mp3_15s_es, convert=False)
        genrec.recognize()

    @nose.raises(FileDoesNotExistError)
    def test_nonexistent_file(self):
        genrec = GenderRecognizer('/herp/derp.wav')
        genrec.recognize()
