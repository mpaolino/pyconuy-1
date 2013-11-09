# -*- coding: utf-8 -*-
from nose import tools as nose
from os import path
import mock
import unittest

from pyker import (GenderRecognizer, InsufficientDataError,
                   ServerError)
from .mocks import (requests_mock, need_more_mock,
                    something_went_wrong_mock)


class ConvertionTests(unittest.TestCase):
    def setUp(self):
        cwd = path.dirname(__file__)
        # Thanks to https://www.youtube.com/watch?v=_mREmb17KW8
        self.mp3_15s_es = path.join(cwd, 'source-15s-es.mp3')
        self.wav_09s_es = path.join(cwd, 'source-09s-es.wav')
        self.wav_15s_es = path.join(cwd, 'source-15s-es.wav')

    @mock.patch('requests.post', new=requests_mock)
    def test_file_conversion(self):
        genrec = GenderRecognizer(self.mp3_15s_es)
        result = genrec.recognize(async=False)

        nose.eq_(result, GenderRecognizer.FEMALE)
        nose.eq_(genrec.is_female(), True)

    @nose.raises(InsufficientDataError)
    @mock.patch('requests.post', new=need_more_mock)
    def test_short_audio(self):
        genrec = GenderRecognizer(self.wav_09s_es)
        genrec.recognize()

    @nose.raises(ServerError)
    @mock.patch('requests.post', new=something_went_wrong_mock)
    def test_server_error(self):
        genrec = GenderRecognizer(self.wav_15s_es)
        genrec.recognize()


# This set of tests will actually hit the server
class GenderRecognizerTests(unittest.TestCase):
    def setUp(self):
        cwd = path.dirname(__file__)
        # Thanks to https://www.youtube.com/watch?v=_mREmb17KW8
        self.wav_09s_es = path.join(cwd, 'source-09s-es.wav')
        self.wav_15s_es = path.join(cwd, 'source-15s-es.wav')

    def test_gender_recognition(self):
        genrec = GenderRecognizer(self.wav_15s_es)
        result = genrec.recognize(async=False)

        nose.eq_(result, GenderRecognizer.FEMALE)
        nose.eq_(genrec.is_female(), True)

    @nose.raises(InsufficientDataError)
    def test_short_audio(self):
        genrec = GenderRecognizer(self.wav_09s_es)
        genrec.recognize()
