# -*- coding: utf-8 -*-
import subprocess
import tempfile
import wave

from pyker.exceptions import ConversionError, InsufficientDataError


class AudioFormatChecker(object):
    """
    Receives an audio and checks that it's the correct format as defined by the
    Expand Voice Recognition API.
    """

    SUPPORTED_FORMATS = (
        'wav',
    )

    def __init__(self, file_path):
        self.file_path = file_path

    def needs_conversion(self):
        """
        The needs_conversion() method will perform all the actual checks for
        the validity of the audio file that will be supplied to the XVR API.
        When those restrictions change, this method will need to be updated.
        """

        extension = self.file_path.split('.')[-1]
        if extension not in self.SUPPORTED_FORMATS:
            return True

        try:
            audio = wave.open(self.file_path)
        except:
            return True

        if audio.getnchannels() != 1:
            return True

        if audio.getframerate() != 8000:
            return True

        if audio.getsampwidth() != 2:
            return True

        if audio.getnframes() < 80000:
            raise InsufficientDataError()

        return False


class Converter(object):
    """
    Takes care of conversion of audio formats.

    This class has an optional dependency with ffmpeg. If found, it
    will be used to convert the input files into the correct format,
    but if the software is not installed (and the file is not in the
    expected format) it will just fail gracefully.
    """

    def __init__(self, audio_path):
        self.audio_path = audio_path
        self.converter_path = None

    def converter_available(self):
        return bool(self.get_converter_path())

    def get_converter_path(self):
        """
        Returns the path to the ffmpeg binary, or None if not installed.
        """

        if self.converter_path:
            return self.converter_path

        cmd = ['which', 'ffmpeg']
        call = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        path = call.stdout.read().strip()

        if path:
            self.converter_path = path

        return self.converter_path

    def convert(self):
        """
        ffmpeg -i /path/file.mp3 -ac 1 -ar 8000 -f wav /tmp/file.wav
        """
        ffmpeg = self.get_converter_path()
        output_file = tempfile.NamedTemporaryFile(suffix='.wav')
        output_file.close()
        cmd = [ffmpeg, '-i', self.audio_path, '-ac', '1', '-ar', '8000',
               '-f', 'wav', output_file.name]

        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)

        if proc.wait() != 0:
            raise ConversionError(proc)

        return output_file.name
