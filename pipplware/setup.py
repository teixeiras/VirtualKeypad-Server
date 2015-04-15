#!/usr/bin/env python

from setuptools import setup, Extension

setup(name='pipplware',
      version='1.0.4',
      description='pipplware daemon with multiple funcitions',
      author='Filipe Teixeira',
      author_email='teixeiras@gmail.com',
      url='http://www.techtux.org/',
      packages=['pipplware',
                'pipplware.web',
                'pipplware.web.sensors',
                'pipplware.web.transmissionrpc',
                'pipplware.web.vcgencmd',
                'pipplware.web.xbmcjson',
                'pipplware.web.transmissionrpc',
                'pipplware.web.bottle_websocket',
                'pipplware.web.bottle_websocket.geventwebsocket',
                'pipplware.piSession',
                'pipplware.pipServices',
                'pipplware.pipInput'
                ],
      entry_points = {
        'console_scripts':['pipplware=pipplware:main']
    },
    data_files=[('/etc/pipplware/', ['files/daemon.cfg']),
                ('/etc/init.d/', ['files/init/pipplware']),
                ('/etc/udev/rules.d/', ['files/udev/40-wifi.rules','files/udev/40-pipplware.rules'])],

 )