__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '15/02/19'


class BadRequestError(Exception):
    def __init__(self, message):
        super(BadRequestError, self).__init__(message)
