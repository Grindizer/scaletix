#!/usr/bin/env python
# -*- coding: utf-8 -*-

from twisted.internet.protocol import ServerFactory, Protocol
from scaletix.worker import ProcessWorker


class ScaleProtocol(Protocol):
    def connectionMade(self):
        self.factory.i += 1
        worker = self.factory.workers[self.factory.i % 2]  #dispatch_strategy.get_next()
        worker.handle_connection(self.transport.getHandle())


# TODO: LoadBalancing strategy
class ScaleFactory(ServerFactory):
    """ Wrap a twisted factory.
    The result is a factory that run the base server protocol in a pool of worker (process)
    The result protocol dispatch the client request to each instances according to a LoadBalancing Strategy.
    """

    protocol = ScaleProtocol
    #TODO: implement dispatcher strategy.
    i = -1

    #TODO: make core default value = nbr_core - 1 (may be)
    def __init__(self, base_factory, core=2):
        self.base_factory = base_factory
        self.core = core
        self.workers = []

    def startFactory(self):
        self.workers = [ProcessWorker(self.base_factory) for i in range(self.core)]

        for worker in self.workers:
            worker.start()

    def stopFactory(self):
        for worker in self.workers:
            worker.terminate()



