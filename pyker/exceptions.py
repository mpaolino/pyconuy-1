# -*- coding: utf-8 -*-


class ConversionError(Exception):
    def __init__(self, proc):
        print(proc.stderr.read())
        msg = ('The conversion software exited with code '
               '%s' % proc.returncode)

        super(ConversionError, self).__init__(self, msg)


class FileDoesNotExistError(Exception):
    def __init__(self, path):
        msg = "The file '%s' does not exist" % path

        super(FileDoesNotExistError, self).__init__(self, msg)


class UnsupportedFormatError(Exception):
    def __init__(self, ext):
        msg = "The format '%s' is currently unsupported." % ext

        super(UnsupportedFormatError, self).__init__(self, msg)


class ServerError(Exception):
    def __init__(self, response):
        msg = 'Server returned %s %s: %s' % (
            response.status_code, response.reason, response.json())

        super(ServerError, self).__init__(self, msg)


class InsufficientDataError(Exception):
    def __init__(self):
        msg = 'Not enough data.'

        super(InsufficientDataError, self).__init__(msg)
