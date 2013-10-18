#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket

from twisted.internet.protocol import ServerFactory, Protocol
from scaletix.dispatcher import RoundRobinDispatcher
from scaletix.worker import ProcessWorker


class ScaleProtocol(Protocol):
    def connectionMade(self):
        worker = self.factory.dispatch_strategy.get_next()
        worker.handle_connection(self.transport.getHandle())


class ScaleFactory(ServerFactory):
    """ Wrap a twisted factory.
    The result is a factory that run the base server protocol in a pool of worker (process)
    The result protocol dispatch the client request to each instances according to a LoadBalancing Strategy.
    """

    protocol = ScaleProtocol
    dispatch_strategy = None
    _workers = []

    #TODO: make core default value = nbr_core - 1 (may be)
    def __init__(self, base_factory, core=2):
        self.base_factory = base_factory
        self.core = core

    def startFactory(self):
        #FIX: FileExistError pb.
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._workers = [ProcessWorker(self.base_factory) for i in range(self.core)]
        #self.dispatcher = self.dispatcher_strategy(self.workers)
        self.dispatch_strategy = RoundRobinDispatcher(self._workers)

        #for worker in self.workers:
        #    worker.start()

    def stopFactory(self):
        for worker in self._workers:
            worker.terminate()



