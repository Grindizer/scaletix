===============================
scaletix
===============================

.. image:: https://badge.fury.io/py/scaletix.png
    :target: http://badge.fury.io/py/scaletix
    
.. image:: https://travis-ci.org/grindizer@gmail.com/scaletix.png?branch=master
        :target: https://travis-ci.org/grindizer@gmail.com/scaletix

.. image:: https://pypip.in/d/scaletix/badge.png
        :target: https://crate.io/packages/scaletix?version=latest


A pure python load balancer for Twisted bases server application.

* Free software: BSD license
* Documentation: TBD

Requirement
-----------

* Python >= 3.3
* Twisted >= 13.1.0
* psutils only if LeastBusyDispatcher is needed.

Example
-------

This will scale the twisted HTTP server to run over a pool of 3 process.

::

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
    reactor.listenTCP(8080, scaled_site)

    reactor.run()


How does it work
----------------

Each time a client connect to the server, the resulting socket is passed over to one of the workers using "sendmsg".

And thus, the load balancer do not work by redirecting data that it receives, but it rather passes over the socket to one of the workers and let it handle all read and write operations.


Features
--------

* TODO