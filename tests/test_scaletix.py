#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_scaletix
----------------------------------

Tests for `scaletix` module.
"""
import time

from twisted.internet import reactor
from twisted.internet.defer import gatherResults, Deferred

from twisted.trial import unittest

from scaletix.factory import ScaleFactory
from tests.test_application import TestFactory
from tests.test_application import TestClientFactory


class TestTCPScaletix(unittest.TestCase):

    def setUp(self):
        pass

    def test_multiprocessing_factory(self):
        # Wrap the TestFactory.
        mp_factory = ScaleFactory(TestFactory(), core=2)
        # launch the new multiprocessing factory
        port = reactor.listenTCP(8118, mp_factory)

        # connect twice to the new server and check that
        # instances server run into different process'
        client_factory = TestClientFactory()
        client_factory.client_deferred_list = [Deferred(), Deferred()]
        time.sleep(1)
        cl1 = reactor.connectTCP('localhost', 8118, client_factory)
        cl2 = reactor.connectTCP('localhost', 8118, client_factory)

        result = gatherResults(client_factory.client_deferred_list)
        def check_result(r_list):
            self.assertEqual(len(r_list), 2, "Both client should have been called. ({0})".format(repr(r_list)))
            self.assertTrue(r_list[0][0] != r_list[1][0], """pid returned from the first client should be different from
            the one returned by the second client""")

            self.assertTrue(r_list[0][1] == b'0')
            self.assertTrue(r_list[1][1] == b'1')

        result.addCallback(check_result)
        self.addCleanup(self._clean_reactor, [port], [cl1, cl2])
        return result

    def _clean_reactor(self, ports, clients):
        for p in ports:
            p.stopListening()

        for client in clients:
            client.transport.loseConnection()


    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()