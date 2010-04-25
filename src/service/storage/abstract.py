# coding: utf-8

class Storage(object):
    
    def add_room_message(self, message):
        """ Add message """
    
    def add_private_message(self, message):
        """ Add private message """
    
    def add_system_message(self, message):
        """ Add system message """
    
    def get_messages(self, flags, username, room_id, lmi, lpi, lsi):
        """ Get messages for target username in target room_id """
