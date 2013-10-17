
from multiprocessing import Process
import os
import socket
from struct import pack, unpack
from twisted.internet import reactor
from zope.interface import implementer
from scaletix.interface import IWorker

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
        return "WORKER-%s: " % os.getpid()


class WorkerProtocol():
    # IWorker Protocol has an original factory field ?!
    def __init__(self, original_factory):
        self.original_factory = original_factory

    def fd_received(self, fd, message):
        print("fd (%s) Received by worker [%s]" % (fd, os.getpid()))
        reactor.adoptStreamConnection(fd, socket.AF_INET, self.original_factory)


@implementer(IWorker)
class ProcessWorker(object):

    def __init__(self, cf):
        self.manager, self.worker = socket.socketpair()
        self.factory = cf
        self.process = Process(target=self._worker_run, args=(self.worker,))
        self.process.start()

    def _worker_run(self, my_sock):
        print("Worker ready [%s]" % os.getpid())
        recvmsg_receiver = WorkerConnection(my_sock, WorkerProtocol(self.factory))

        reactor.addReader(recvmsg_receiver)
        reactor.run()

    #TODO: replace this blocking call! (doWrite)
    def handle_connection(self, sock, message=b'a message'):
        self.manager.sendmsg([message], [(socket.SOL_SOCKET, socket.SCM_RIGHTS, pack('i', sock.fileno()))])
        # close socket on the load balancer process (parent).
        sock.close()

    def start(self):
        self.process.start()

    def terminate(self):
        self.manager.close()
        self.process.terminate()