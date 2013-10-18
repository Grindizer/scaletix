import heapq
import random
from zope.interface import implementer
from scaletix.interface import IDispatchStrategy

__author__ = 'nacim'

@implementer(IDispatchStrategy)
class RoundRobinDispatcher(object):
    def __init__(self, workers):
        self.workers = workers
        self._i = -1

    def get_next(self, data=None):
        self._i += 1
        return self.workers[self._i % len(self.workers)]


@implementer(IDispatchStrategy)
class RandomDispatcher(object):
    def __init__(self, workers):
        self.workers = workers

    def get_next(self, data=None):
        return random.choice(self.workers)

