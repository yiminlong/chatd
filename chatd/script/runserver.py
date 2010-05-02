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
parser.add_option("-p", "--port", dest="port", type="int", default=1135,
                  help="use PORT to listen incoming connections "
                  "(default is 1135)",
                  metavar="PORT")

def append_paths():
    """ Add chatd directory to sys.path. """
    chatd_path = os.path.normpath(
                            os.path.join(os.path.abspath(__file__), *['..']*3))
    if chatd_path not in sys.path:
        sys.path.append(chatd_path)

def set_loggers(verbose):
    if not verbose:
        return
    
    import logging
    logger = logging.getLogger("chatd")
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter("[%(asctime)s] %(name)s %(levelname)s: %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    logging.getLogger("chatd.script.runserver").info("Initializing server in verbose mode.")

def init_settings(storage, verbose):
    from chatd.service.config import Settings
    settings = Settings()
    settings.set_storage(storage)
    settings.set_verbose(verbose)

def run_reactor(port):
    from twisted.internet import reactor
    from chatd.server.factory import ChatServerFactory
    reactor.listenTCP(port, ChatServerFactory())
    reactor.run()

def execute():
    options, args = parser.parse_args()
    
    set_loggers(options.verbose)
    init_settings(options.storage, options.verbose)
    run_reactor(options.port)

if __name__ == "__main__":
    append_paths()
    execute()
