# coding: utf-8

from twisted.internet.protocol import ServerFactory
from chatd.server.protocol import ChatServerProtocol

class ChatServerFactory(ServerFactory):
    """ Simple ChatServer factory """
    
    protocol = ChatServerProtocol
