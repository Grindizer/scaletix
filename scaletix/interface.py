from zope.interface import Interface, Attribute

__author__ = 'nacim'

class IWorker(Interface):
    id = Attribute("worker unique identifier")
    def start():
        """ """

    def terminate():
        """ """

    def handle_connection(socket):
        """ pass the socket to this worker """