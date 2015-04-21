from distutils.core import setup
import os
from setuptools import setup
from suggest import __version__
with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='suggest',
    version=__version__,
    packages=[
        'suggest',
        'suggest.data',
        'suggest.handlers',
        'suggest.logic'
    ],
    install_requires=required
)
