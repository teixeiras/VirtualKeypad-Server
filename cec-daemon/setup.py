#!/usr/bin/env python

from setuptools import setup, Extension

setup(name='pipCec',
      version='1.0.4',
      description='Pipplware cec',
      author='Filipe Teixeira',
      author_email='teixeiras@gmail.com',
      url='http://www.techtux.org/',
      packages=['pipCec'],
      entry_points = {
        'console_scripts':['cec-daemon=pipCec:main']
    },
    data_files=[('/etc/init.d/', ['files/init/cec'])],

 )