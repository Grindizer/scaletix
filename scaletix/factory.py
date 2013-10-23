#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import socket

from twisted.internet.protocol import ServerFactory, Protocol
from scaletix.dispatcher import RoundRobinDispatcher
from scaletix.worker import Worker

#TODO: add logging capability (twisted.python.log)
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
    def __init__(self, base_factory, core=2, dispatcher_factory=RoundRobinDispatcher):
        self.base_factory = base_factory
        self.dispatcher_factory = dispatcher_factory
        self.core = core

    def startFactory(self):
        #FIX: FileExistError pb, still with epollreactor ! https://twistedmatrix.com/trac/ticket/6796
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._workers = [Worker(self.base_factory) for i in range(self.core)]
        self.dispatch_strategy = self.dispatcher_factory(self._workers)

    def stopFactory(self):
        for worker in self._workers:
            worker.terminate()



