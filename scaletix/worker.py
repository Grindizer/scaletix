
from multiprocessing import Process
import os
import socket
from struct import pack, unpack
import psutil
from twisted.internet import reactor
from zope.component import adapter
from zope.interface import implementer
from scaletix.interface import IWorker, IUsageStat

__author__ = 'nacim'


class WorkerConnection():
    # protocol ==> IWorkerProtocol ?!
    # socket of type UNIX only.
    def __init__(self, usocket, protocol):
        self.sock = usocket
        self.protocol = protocol

    def doRead(self):
        msg, ancillary, flags, addr = self.sock.recvmsg(1024, 1024)
        for anc in ancillary:
            if anc[1] == socket.SCM_RIGHTS:
                fd = unpack('i', anc[2])[0]
                self.protocol.fd_received(fd, msg)

    def fileno(self):
        return self.sock.fileno()

    def connectionLost(self, reason):
        self.sock.close()

    def logPrefix(self):
        return "WORKER-{0}: ".format(os.getpid())


class WorkerProtocol():
    # IWorker Protocol has an original factory field ?!
    def __init__(self, original_factory):
        self.original_factory = original_factory

    def fd_received(self, fd, message):
        print("fd ({0}) Received by worker [{1}]".format(fd, os.getpid()))
        reactor.adoptStreamConnection(fd, socket.AF_INET, self.original_factory)

class WorkerProcess(Process):
    def __init__(self, factory, pipe):
        super(WorkerProcess, self).__init__()
        self.factory = factory
        self.pipe = pipe

    def run(self):
        print("Process Worker [{0}] ready".format(os.getpid()))
        recvmsg_receiver = WorkerConnection(self.pipe, WorkerProtocol(self.factory))

        reactor.addReader(recvmsg_receiver)
        reactor.run()

@implementer(IWorker)
class Worker(object):
    def __init__(self, cf):
        self.manager, worker = socket.socketpair()

        self.factory = cf
        self.nbr_handle = 0
        self.process = WorkerProcess(self.factory, worker)
        self.process.start()


    #TODO: replace this blocking call! (doWrite)
    def handle_connection(self, sock, message=b'a message'):
        self.manager.sendmsg([message], [(socket.SOL_SOCKET, socket.SCM_RIGHTS, pack('i', sock.fileno()))])
        # close socket on the load balancer process (parent).
        self.nbr_handle += 1
        sock.close()

    @property
    def id(self):
        return self.process.pid


    def start(self):
        self.process.start()

    def terminate(self):
        self.manager.close()
        self.process.terminate()

@implementer(IUsageStat)
@adapter(IWorker)
class WorkerUsage(object):
    def __init__(self, worker):
        self.worker = worker
        #TODO: check if we have to use an asynchronous version of the psutil lib ?!
        self.proc = psutil.Process(self.worker.id)

    def get_connections(self):
        return self.proc.get_connections()

    def get_cpu_times(self):
        return self.proc.get_cpu_times()

    def get_cpu_usage(self):
        return self.proc.get_cpu_percent(interval=0) / 100.0

    def get_memory_usage(self):
        return self.proc.get_memory_info()

    def get_nbr_handled_connections(self):
        return self.worker.nbr_handle