# coding: utf-8

from ..flag import *
from . import abstract
from .utils import ShiftedList

class Storage(abstract.Storage):
    
    def __init__(self):
        self.room_messages = ShiftedList()
        self.private_messages = ShiftedList()
        self.system_messages = ShiftedList()
    
    def add_room_message(self, message):
        self.room_messages.append(message)
    
    def add_private_message(self, message):
        self.private_messages.append(message)
    
    def add_system_message(self, message):
        self.system_messages.append(message)
    
    def get_messages(self, flags, username, room_id, lmi, lpi, lsi):
        return_messages = []
        
        lmi, lpi, lsi = self._verify_indexes(lmi, lpi, lsi)
        
        return_messages.extend(
                         self._get_room_message(flags, username, room_id, lmi))
        return_messages.extend(self._get_private_messages(username, lpi))
        return_messages.extend(
                      self._get_system_messages(flags, username, room_id, lsi))
        
        return_messages.sort(key = 'time')
        
        return {
                'room_messages': self.room_messages.count(),
                'private_messages': self.private_messages.count(),
                'system_messages': self.system_messages.count(),
                'result_messages': len(return_messages),
            }, (message.text for message in return_messages)
    
    def _verify_indexes(self, lmi, lpi, lsi):
        if self.room_messages.count() < lmi:
            lmi = -30 # i.e. last 30 items
        
        if self.private_messages.count() < lpi:
            lpi = -30
        
        if self.system_messages.count() < lsi:
            lsi = -30
        
        return lmi, lpi, lsi
    
    def _get_room_messages(self, flags, username, room_id, last_message):
        for message in self.room_messages[:last_message]:
            if message.room_id != room_id:
                continue
            
            if flags != PRIVATES_ONLY or \
              message.username == username or username in message.receivers:
                yield message
    
    def _get_private_messages(self, username, last_message):
        for message in self.private_messages[:last_message]:
            if message.username == username or username in message.receivers:
                yield message
    
    def _get_system_messages(self, flags, username, room_id, last_message):
        for message in self.system_messages[:last_message]:
            if username in message.receivers or \
              (flags == SHOW_SYSTEM and message.room_id == room_id):
                yield message
