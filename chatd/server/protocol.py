# coding: utf-8

import logging

from twisted.protocols.basic import LineReceiver

from chatd.service import get_storage
from chatd.service.model import RoomMessage, PrivateMessage, SystemMessage
from chatd.server.exc import RequestFormatError

log = logging.getLogger(__name__)

class ChatServerProtocol(LineReceiver):
    
    def sendLine(self, line):
        if isinstance(line, unicode):
            line = line.encode('utf-8')
        LineReceiver.sendLine(self, line)
    
    def errorResponse(self, error):
        self.sendLine(error)
        self.transport.loseConnection()
    
    def lineReceived(self, line):
        log.debug("Received line: " + line)
        
        operation, request = line.split(' ', 1)
        try:
            method = self._dispatchMethod(operation)
        except ValueError, e:
            self.errorResponse(e.message)
        else:
            method(request)
    
    def callPut(self, request):
        try:
            PutOperationProcessor().process(request)
        except RequestFormatError, e:
            log.error("Error parsing request: " + request, exc_info=True)
            self.errorResponse('error ' + e.message)
        else:
            self.sendLine('added')
    
    def callGet(self, request):
        for response in GetOperationProcessor().process(request):
            self.sendLine(response)
    
    def _dispatchMethod(self, operation):
        if operation == 'put':
            return self.callPut
        elif operation == 'get':
            return self.callGet
        else:
            log.error("Unsupported operation '%s'." % operation)
            raise ValueError("Unsupported operation '%s'" % operation)

class PutOperationProcessor(object):
    
    AVAILABE_TYPES = ('room', 'private', 'system')
    
    def process(self, line):
        log.debug("Invoking PUT operation.")
        
        type, meta, text = line.split(' ', 2)
        if type in self.AVAILABE_TYPES:
            method = getattr(self, 'add%sMessage' % type.capitalize())
            method(*chain(meta.split(':'), [text]))
    
    def addRoomMessage(self, username, room_id, receivers, source_text):
        """ Format::
        'username:room_id:receiver1,receiver2 source message'
        """
        receivers = receivers and receivers.split(',') or []
        
        get_storage().add_room_message(
                        RoomMessage(username, room_id, receivers, source_text))
        return True
    
    def addPrivateMessage(self, username, receivers, source_text):
        """ Format::
        'username:receiver1,receiver2 source message'
        """
        receivers = receivers.split(',')
        
        get_storage().add_private_message(
                              PrivateMessage(username, receivers, source_text))
        return True
    
    def addSystemMessage(self, room_id, receivers, text):
        """ Format::
        'room_id:receiver1,receiver2 compiled message'
        """
        if len(room_id) == 0:
            room_id = None
        
        receivers = receivers and receivers.split(',') or []
        
        if room_id is None and not receivers:
            raise RequestFormatError("Unable to store system message: "
                                     "neither room_id nor receivers provided.")
        
        get_storage().add_system_message(
                                       SystemMessage(room_id, receivers, text))

from itertools import chain

class GetOperationProcessor(object):
    
    META_FORMAT = ' '.join([
                       '%(room_messages)s',
                       '%(private_messages)s',
                       '%(system_messages)s',
                       '%(result_messages)s'
                   ])
    
    def process(self, line):
        log.debug("Invoking GET operation.")
        
        flags, username, room_id, lmi, lpi, lsi = line.split(' ')
        data, messages = get_storage().get_messages(
                                       flags, username, room_id, lmi, lpi, lsi)
        return chain([self._compile_meta(data)], messages)
    
    def _compile_meta(self, data):
        return self.META_FORMAT % data
