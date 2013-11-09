# -*- coding: utf-8 -*-
"""
Mocks of the XVR requests.
"""


class XVRStatusMock(object):

    def __init__(self, status_code=200, gender='F',
                 score='1.34569807', new_result_in=5):
        self.status_code = status_code
        self.gender = gender
        self.score = score
        self.new_result_in = new_result_in

    def json(self):
        return {
            'gender': self.gender,
            'score': self.score,
            'new_result_in': self.new_result_in,
        }


class XVRRecognizeMock(object):

    def __init__(self, status_code=200, reason='OK',
                 received_sequences=[1, 2], new_result_in=5,
                 need_more=False,
                 task_id='bf4f25f6682d4d2990cec25a91a15e75'):
        self.status_code = status_code
        self.reason = reason
        self.received_sequences = received_sequences
        self.new_result_in = new_result_in
        self.need_more = need_more
        self.task_id = task_id

    def json(self):
        return {
            'received_sequences': self.received_sequences,
            'new_result_in': self.new_result_in,
            'need_more': self.need_more,
            'task_id': self.task_id,
        }


def requests_mock(*args, **kwargs):
    if args[0].endswith('gender'):
        return XVRRecognizeMock()
    elif args[0].endswith('result'):
        return XVRStatusMock()


def need_more_mock(*args, **kwargs):
    if args[0].endswith('gender'):
        return XVRRecognizeMock(need_more=True)
    elif args[0].endswith('result'):
        return XVRStatusMock()


def something_went_wrong_mock(*args, **kwargs):
    return XVRRecognizeMock(status_code=500, reason='Server Error')
