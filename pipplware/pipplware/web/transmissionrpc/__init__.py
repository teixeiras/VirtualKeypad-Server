# -*- coding: utf-8 -*-
# Copyright (c) 2008-2014 Erik Svensson <erik.public@gmail.com>
# Licensed under the MIT license.

from pipplware.web.transmissionrpc.constants import DEFAULT_PORT, DEFAULT_TIMEOUT, PRIORITY, RATIO_LIMIT, LOGGER
from pipplware.web.transmissionrpc.error import TransmissionError, HTTPHandlerError
from pipplware.web.transmissionrpc.httphandler import HTTPHandler, DefaultHTTPHandler
from pipplware.web.transmissionrpc.torrent import Torrent
from pipplware.web.transmissionrpc.session import Session
from pipplware.web.transmissionrpc.client import Client
from pipplware.web.transmissionrpc.utils import add_stdout_logger, add_file_logger

__author__    		= 'Erik Svensson <erik.public@gmail.com>'
__version_major__   = 0
__version_minor__   = 12
__version__   		= '{0}.{1}'.format(__version_major__, __version_minor__)
__copyright__ 		= 'Copyright (c) 2008-2014 Erik Svensson'
__license__   		= 'MIT'