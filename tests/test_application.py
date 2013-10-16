#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
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
    ID = -1

    def connectionMade(self):
        TestClientProtocol.ID += 1
        self.id = TestClientProtocol.ID
        data = bytes(str(self.id).encode('utf8'))
        self.transport.write(data)

    def dataReceived(self, line):
        pid, client_id = line.split(b':')
        self.factory.client_deferred_list[self.id].callback((pid, client_id))


class TestClientFactory(ClientFactory):
    protocol = TestClientProtocol
    client_deferred_list = []




