import heapq
import random
from zope.interface import implementer
from scaletix.interface import IDispatchStrategy
from scaletix.worker import WorkerUsage

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

#TODO: Write dispatcher that work from nbr_handled_connections.
@implementer(IDispatchStrategy)
class LeastBusyDispatcher(object):
    def __init__(self, workers):
        self.workers = workers
        self.usages = [WorkerUsage(worker) for worker in self.workers]

    def get_next(self, data=None):
        conns = []
        for i, wu in enumerate(self.usages):
            heapq.heappush(conns, (len(wu.get_connections()), i))

        #print("from {0} ==> ".format(conns), end="")
        nb, index = heapq.heappop(conns)
        #print("{0}".format(index))
        return self.usages[index].worker