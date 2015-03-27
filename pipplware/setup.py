#!/usr/bin/env python

from distutils.core import setup

setup(name='pipplware',
      version='1.0',
      description='pipplware daemon with multiple funcitions',
      author='Filipe Teixeira',
      author_email='gward@python.net',
      url='http://www.techtux.org/',
      packages=['pipplware',
                'pipplware.sensors',
                'pipplware.transmissionrpc',
                'pipplware.vcgencmd',
                'pipplware.xbmcjson',
                'pipplware.transmissionrpc',
                'pipplware.web'],
     )