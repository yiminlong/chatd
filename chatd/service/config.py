# coding: utf-8

from chatd.service.storage import abstract

class Settings(object):
    
    _instance = None
    
    def __init__(self):
        if self._instance is not None:
            raise Exception("Settings already instantiated")
        
        self.__class__._instance = self
        self._opts = {}
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            raise Exception("Settings was not instantiated")
        return cls._instance
    
    def set_storage(self, module_name):
        try:
            module = __import__(module_name, fromlist=[''])
        except ImportError, e:
            raise Exception("Module '%s' can not be imported", e)
        
        try:
            print dir(module)
            storage = getattr(module, 'Storage')
        except AttributeError:
            raise Exception("Module '%s' does not contain 'Storage' class")
        
        if not issubclass(storage, abstract.Storage):
            raise Exception("Storage must be a subclass of abstract.Storage")
        
        self._storage = storage()
    
    def set_verbose(self, verbose):
        self._verbose = bool(verbose)
    
    def set(self, option, value):
        self._opts[option] = value
    
    def get_storage(self):
        return self._storage
