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


class IUsageStat(Interface):
    def get_nbr_handled_connections():
        """ return all connections handled till now. (include closed)."""

    def get_connections():
        """ only currently opened connections """

    def get_cpu_times():
        """ """

    def get_cpu_usage():
        """ return cpu usage."""

    def get_memory_usage():
        """ return memory usage (used, available)"""

class IDispatchStrategy(Interface):
    def get_next(data=None):
        """ return next worker to be used to handle the new connection,
        data could be any necessary data collected from first reading the connection and that
        may be useful to chose the worker."""

class IDispatcherFactory(Interface):
    def __call__(workers):
        """ """