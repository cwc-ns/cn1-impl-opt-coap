#!/usr/bin/env python

from setuptools import setup, find_packages

import sys

if sys.version_info.major >= 3:
    VERSION = '0.3.5'
    twisted = ['twisted>=16.4.1']
    ipaddress = ['ipaddress>=1.0.17']
else:
    VERSION = '0.3.0'
    twisted = ['twisted<=16.4.1']
    ipaddress = [ 'py2-ipaddress>=3.4.1' ]

setup(name='txThings',
      version=VERSION,
      description='CoAP protocol implementation for Twisted Framework',
      author='Maciej Wasilak',
      author_email='wasilak@gmail.com',
      url='https://github.com/siskin/txThings/',
      packages=find_packages(exclude=["*.test", "*.test.*"]),
      install_requires = ['six>=1.10.0', 'service_identity>=18.1.0'] + twisted + ipaddress,
     )
