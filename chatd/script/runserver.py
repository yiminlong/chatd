#!/usr/bin/env python

from optparse import OptionParser

import sys
import os

parser = OptionParser()
parser.add_option("-v", "--verbose",
                  action="store_true", dest="verbose", default=False,
                  help="print status messages to stdout")
parser.add_option("-s", "--storage", dest="storage",
                  default="chatd.service.storage.memory",
                  help="use MODULE as message storage provider",
                  metavar="MODULE")
parser.add_option("-p", "--port", dest="port", default="1135",
                  help="use PORT to listen incoming connections "
                  "(default is 1135)",
                  metavar="PORT")

def append_paths():
    """ Add chatd directory to sys.path. """
    chatd_path = os.path.normpath(
                            os.path.join(os.path.abspath(__file__), *['..']*3))
    if chatd_path not in sys.path:
        sys.path.append(chatd_path)

def execute():
    options, args = parser.parse_args()
    
    from chatd.service.config import Settings
    settings = Settings()
    settings.set_verbose(options.verbose)
    settings.set_storage(options.storage)
    
    from twisted.internet import reactor
    from chatd.server.factory import ChatServerFactory
    reactor.listenTCP(int(options.port), ChatServerFactory())
    reactor.run()

if __name__ == "__main__":
    append_paths()
    execute()
