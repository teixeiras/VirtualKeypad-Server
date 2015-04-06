#!/usr/bin/env python

from setuptools import setup

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
                'pipCec',
                'pipInput'
                ],
      entry_points = {
        'console_scripts' : ['pipplware = pipplware.pipplware:main',
                             'cec-daemon = pipCec.pipCec:main']
    },
    data_files=[('/etc/pipplware/', ['daemon.cfg']),
                ('/etc/init.d/', ['files/init/cec','files/init/pipplware'])]

 )