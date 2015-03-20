from distutils.core import setup
import os
from setuptools import setup

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='suggest',
    version='0.0.1',
    packages=[
        'suggest',
        'suggest.data',
        'suggest.handlers',
        'suggest.workers'
    ],
    install_requires=required
)
