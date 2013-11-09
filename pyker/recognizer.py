# -*- coding: utf-8 -*-
import datetime
import os
import time
import wave

import requests

from pyker.exceptions import (
    UnsupportedFormatError, ServerError, InsufficientDataError,
    FileDoesNotExistError)
from pyker.utils import AudioFormatChecker, Converter


class Audio(object):
    """
    An audio file. Stores all the information related to the file being
    processed.
    """

    def __init__(self, file_path=None, convert=True):
        self.file_path = file_path
        self.dont_convert = not bool(convert)

        self.extension = self.file_path.split('.')[-1]
        self.audio_file = None
        self.checker = None
        self.converter = None

    def load(self):
        """
        This method does all the file-loading necessary to work with the
        object. This is not done at initizliation time to avoid unwanted side
        effects.
        """

        if self.needs_conversion():
            if not self.converter:
                self.converter = Converter(self.file_path)

            if self.can_convert():
                self.file_path = self.convert()
            else:
                raise UnsupportedFormatError(self.extension)

        self.audio_file = wave.open(self.file_path)

    def needs_conversion(self):
        if not self.checker:
            self.checker = AudioFormatChecker(self.file_path)

        return self.checker.needs_conversion()

    def get_contents(self):
        contents = self.audio_file.readframes(self.get_frames())
        self.audio_file.rewind()

        return contents

    def can_convert(self):
        return (not self.dont_convert) and self.converter.converter_available()

    def convert(self):
        return self.converter.convert()

    def get_frame_rate(self):
        return self.audio_file.getframerate()

    def get_bit_depth(self):
        return self.audio_file.getsampwidth() * 8

    def get_channels(self):
        return self.audio_file.getnchannels()

    def get_frames(self):
        return self.audio_file.getnframes()


class GenderRecognizer(object):
    """
    Interface with Expand's Voice Recognition API.
    """

    MALE = 'M'
    FEMALE = 'F'
    XVR_URL = 'http://voiceapi.expand.com.uy'
    TIMEOUT = 10  # Seconds

    def __init__(self, audio=None, convert=True, task_id=None,
                 sequence_number=1):
        self.convert = bool(convert)
        self.task_id = task_id

        self.result = None
        self.requested_on = None

        self.set_audio(audio)  # Path or file-object
        self.set_sequence_number(sequence_number)

    def set_audio(self, audio):
        path = audio
        if hasattr(audio, 'read'):
            path = audio.name

        if not os.path.exists(path):
            raise FileDoesNotExistError(path)

        self.audio = Audio(path, convert=self.convert)

    def set_sequence_number(self, value):
        self.sequence_number = int(value)

    def get_sequence_number(self):
        return self.sequence_number

    def recognize(self, async=True):
        """
        Does the actual recognition. If the parameter async is False, it will
        loop and poll the server for the result, and continue when it gets it,
        or when it times out.
        """

        self.audio.load()

        voice = {
            'file': self.audio.get_contents(),
        }
        options = {
            'audio_sequence': self.get_sequence_number(),
            'audio_samplerate': self.audio.get_frame_rate(),
            'audio_bitdepth': self.audio.get_bit_depth(),
            'audio_channels': self.audio.get_channels(),
            'audio_sent_frames': self.audio.get_frames(),
        }

        if self.task_id:
            options['task_id'] = self.task_id

        self.requested_on = datetime.datetime.now()
        response = requests.post(self.XVR_URL + '/recognize/gender',
                                 data=options, files=voice)
        self.task_id = response.json()['task_id']

        if response.status_code != 200:
            raise ServerError(response)

        if response.json()['need_more'] == True:
            raise InsufficientDataError()

        if not async:
            self._wait_for_result(response.json()['new_result_in'])

        return self.result

    def _wait_for_result(self, how_long):
        while not self.result:
            try:
                time.sleep(how_long)
            except:
                break

            if not self.get_result():
                timedelta = datetime.datetime.now() - self.requested_on
                if timedelta.seconds > self.TIMEOUT:
                    break

    def is_male(self):
        return self.result == self.MALE

    def is_female(self):
        return self.result == self.FEMALE

    def recognition_complete(self):
        return self.result != None

    def get_result(self):
        if self.result:
            return self.result

        url = self.XVR_URL + '/recognize/gender/result'
        data = {
            'task_id': self.task_id,
        }
        response = requests.post(url, data=data)

        if response.json()['gender'] in ('F', 'M'):
            self.result = response.json()['gender']

        return self.result
