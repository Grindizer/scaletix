import socket

__author__ = 'nacim'

from twisted.trial import unittest
from scaletix.worker import Worker, WorkerUsage

class TestWorkerUsage(unittest.TestCase):
    def setUp(self):
        self.worker = Worker("factory")
        self.wu = WorkerUsage(self.worker)

    def test_get_connection(self):
        self.assertIsInstance(self.wu.get_connections(), list)

    def test_cpu_time(self):
        cputime = self.wu.get_cpu_times()
        self.assertIsInstance(cputime, tuple)
        user, system = cputime
        self.assertIsInstance(user, float)

    def test_cpu_usage(self):
        usage = self.wu.get_cpu_usage()
        self.assertTrue(0.0 <= usage <= 1.0)

    def test_memory_usage(self):
        usage = self.wu.get_memory_usage()
        self.assertIsInstance(usage, tuple)
        used, all = usage
        self.assertTrue(used <= all)

    def tearDown(self):
        self.wu.worker.terminate()
