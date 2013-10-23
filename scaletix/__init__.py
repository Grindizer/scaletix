#!/usr/bin/env python
# -*- coding: utf-8 -*-
from twisted.internet.error import ReactorAlreadyInstalledError

__author__ = 'Nacim B5'
__email__ = 'grindizer@gmail.com'
__version__ = '0.1.0'

from twisted.internet import pollreactor
try:
    pollreactor.install()
except ReactorAlreadyInstalledError:
    pass
