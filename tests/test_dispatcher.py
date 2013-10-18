from unittest import TestCase
from scaletix.dispatcher import RoundRobinDispatcher, RandomDispatcher

__author__ = 'nacim'


class TestDispatcherRound(TestCase):
    def setUp(self):
        self.dispatcher = RoundRobinDispatcher(["w1", "w2"])

    def test_round_robin(self):
        self.assertEqual(self.dispatcher.get_next(), "w1")
        self.assertEqual(self.dispatcher.get_next(), "w2")

    def test_round_robin_return_to_zero(self):
        self.assertEqual(self.dispatcher.get_next(), "w1")
        self.assertEqual(self.dispatcher.get_next(), "w2")
        self.assertEqual(self.dispatcher.get_next(), "w1")
        self.assertEqual(self.dispatcher.get_next(), "w2")


class TestDispatcherRandom(TestCase):
    def setUp(self):
        self.workers = ["w1", "w2"]
        self.dispatcher = RandomDispatcher(self.workers)

    def test_return_a_worker(self):
        self.assertIn(self.dispatcher.get_next(), self.workers)
        self.assertIn(self.dispatcher.get_next(), self.workers)


#TODO: write test for a dispatcher using nbr open connections.


