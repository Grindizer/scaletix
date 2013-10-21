from twisted.internet import reactor
from twisted.internet.defer import gatherResults, Deferred
from twisted.trial.unittest import TestCase
from scaletix.dispatcher import RoundRobinDispatcher, RandomDispatcher, LeastBusyDispatcher
from scaletix.factory import ScaleFactory
from tests.test_application import TestFactory, TestClientFactory

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


class TestDispatcherMinOpenConnection(TestCase):
    def setUp(self):
        self.base_factory = TestFactory()
        self.scale_factory = ScaleFactory(self.base_factory, core=2, dispatcher_factory=LeastBusyDispatcher)

        self.port = reactor.listenTCP(8118, self.scale_factory)
        self.clients = []

    def test_justCheckDispatcherDontReturnError(self):

        client_factory = TestClientFactory()
        client_factory.client_deferred_list = []
        for i in range(10):
            cl1 = reactor.connectTCP('localhost', 8118, client_factory)
            client_factory.client_deferred_list.append(Deferred())
            self.clients.append(cl1)

        self.addCleanup(self._clean_reactor)
        result = gatherResults(client_factory.client_deferred_list)
        return result

    test_justCheckDispatcherDontReturnError.timeout = 5


    def _clean_reactor(self):
        self.port.stopListening()

        for client in self.clients:
            client.disconnect()