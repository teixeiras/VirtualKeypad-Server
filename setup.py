#!/usr/bin/env python

from distutils.core import setup

setup(name='pipplware',
      version='1.0.2',
      description='pipplware daemon with multiple funcitions',
      author='Filipe Teixeira',
      author_email='gward@python.net',
      url='http://www.techtux.org/',
      packages=['pipplware',
                'pipplware.web',
                'pipplware.web.sensors',
                'pipplware.web.transmissionrpc',
                'pipplware.web.vcgencmd',
                'pipplware.web.xbmcjson',
                'pipplware.web.transmissionrpc',
                ],
      entry_points = {
        'console_scripts' : ['pipplware = pipplware.pipplware:main']
    },
    data_files=[('/etc/pipplware/', ['deamon.cfg'])]

 )