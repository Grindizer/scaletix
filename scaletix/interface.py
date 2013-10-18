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

#TODO: implement iusagestat adapter for worker (using psutil ?).
class IUsageStat(Interface):
    def get_nbr_handled_connections():
        """ """

    def get_connections():
        """ """

    def get_uptime():
        """ """

    def get_resource_usage():
        """ """

class IDispatchStrategy(Interface):
    pass