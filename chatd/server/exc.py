# coding: utf-8

class ChatdException(Exception):
    """ Base chatd exception. """

class RequestFormatError(ChatdException):
    """ Chat request can not be parsed """
