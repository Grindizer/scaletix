from twisted.internet import reactor
from scaletix.factory import ScaleFactory
from tests.test_application import TestFactory

__author__ = 'nacim'

if __name__ == '__main__':
    mp_factory = ScaleFactory(TestFactory(), core=2)
    # launch the new multiprocessing factory
    port = reactor.listenTCP(8118, mp_factory)
    reactor.run()
