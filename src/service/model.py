# coding: utf-8

from datetime import datetime

__all__ = ('RoomMessage', 'PrivateMessage', 'SystemMessage')

class _Message(object):
    """ Base abstract message. """
    
    def __init__(self):
        self.time = datetime.now()

class RoomMessage(_Message):
    """ Simple user chat message. """
    
    def __init__(self, username, room_id, receivers, source_text):
        super(RoomMessage, self).__init__()
        
        self.username = username
        self.room_id = room_id
        self.receivers = receivers
        self.source_text = source_text
        
        self.text = self._compile()
    
    def _compile(self):
        return (self.receivers and '%s [%s] %s' or '%s [%s]: %s') % \
                 (self.time.strftime('%H:%M'), self.username, self.source_text)

class PrivateMessage(_Message):
    """ Private message from one user to some others. """
    
    def __init__(self, username, receivers, source_text):
        super(PrivateMessage, self).__init__()
        
        self.username = username
        self.receivers = receivers
        self.source_text = source_text
        
        self.text = self._compile()
    
    def _compile(self):
        return '%s [%s] %s' % \
                 (self.time.strftime('%H:%M'), self.username, self.source_text)

class SystemMessage(_Message):
    """ System message."""
    
    def __init__(self, room_id, receivers, text):
        """ @param room_id: room id. Can be None.
        @param receivers: receivers list. Can be None.
        @param text: compiled message text.
        """
        super(SystemMessage, self).__init__()
        
        self.room_id = room_id
        self.receivers = receivers
        self.text = text
