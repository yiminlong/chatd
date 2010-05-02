# coding: utf-8

from chatd.service.config import Settings

def get_storage():
    """ Return registered chat storage. """
    return Settings.get_instance().get_storage()
