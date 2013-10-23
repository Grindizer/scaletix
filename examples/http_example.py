__author__ = 'nacim'
# use pollreactor, because of an epoll issue when used with multiprocessing !
# https://twistedmatrix.com/trac/ticket/6796
from twisted.internet import pollreactor
pollreactor.install()

from twisted.web import server, resource
from twisted.internet import reactor
from twisted.python import log
import os
import sys

# Import ScaleFactory
from scaletix.factory import ScaleFactory


class Simple(resource.Resource):
    isLeaf = True
    def render_GET(self, request):
        return "<html>Hello, world! from process [{0}]</html>".format(os.getpid()).encode('utf8')


log.startLogging(sys.stdout)

site = server.Site(Simple())
scaled_site = ScaleFactory(site, core=3)

# and then just replace this
# reactor.listenTCP(8081, site)
# by

reactor.listenTCP(8080, scaled_site)

reactor.run()
