#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from twisted.internet import reactor
from twisted.protocols.basic import LineReceiver

__author__ = 'nacim'

from twisted.internet.protocol import Factory, ClientFactory


class TestProtocol(LineReceiver):
    def dataReceived(self, data):
        # get process ID
        uid = os.getpid()
        self.transport.write(bytes(str(uid).encode('utf8')) + b":" + data)


class TestFactory(Factory):
    protocol = TestProtocol


class TestClientProtocol(LineReceiver):

    def connectionMade(self):
        self.factory.ID += 1
        self.id = self.factory.ID
        data = bytes(str(self.id).encode('utf8'))
        self.transport.write(data)
        def fire_error(d):
            d.errback()

        self.r = reactor.callLater(2, fire_error, self.factory.client_deferred_list[self.id])

    def dataReceived(self, line):
        pid, client_id = line.split(b':')
        self.factory.client_deferred_list[self.id].callback((pid, client_id))
        self.r.cancel()


class TestClientFactory(ClientFactory):
    def __init__(self):
        super(ClientFactory, self).__init__()
        self.ID = -1

    protocol = TestClientProtocol
    client_deferred_list = []




