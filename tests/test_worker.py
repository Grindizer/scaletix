import socket

__author__ = 'nacim'

from twisted.trial import unittest
from scaletix.worker import Worker, WorkerUsage

class TestWorkerUsage(unittest.TestCase):
    def setUp(self):
        self.worker = Worker("factory")
        self.wu = WorkerUsage(self.worker)

    def test_get_connection_empty(self):
        self.assertEqual(len(self.wu.get_connections()), 0)

    def tearDown(self):
        self.wu.worker.terminate()
