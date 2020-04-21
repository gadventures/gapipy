#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

import gapipy

# build the long description from the *.RST files
readme = open('README.rst').read()
contributing = open('CONTRIBUTING.rst').read().replace('.. :contributing:', '')
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

long_description = readme + '\n\n' + contributing + '\n\n' + history

requirements = []
with open('requirements.txt') as reqs:
    lines = reqs.readlines()
    for line in lines:
        if line:
            requirements.append(line.strip('\n'))

test_requirements = [
    'mock',
    'nose',
    'nose-parameterized',
]

setup(
    name='gapipy',
    version=gapipy.__version__,
    description='Python client for the G Adventures REST API',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    author='G Adventures',
    author_email='software@gadventures.com',
    url='https://github.com/gadventures/gapipy',
    packages=find_packages(exclude=('tests',)),
    package_dir={'gapipy': 'gapipy'},
    include_package_data=True,
    install_requires=requirements,
    license='MIT',
    zip_safe=False,
    keywords='gapipy',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    test_suite='nose.collector',
    tests_require=test_requirements,
)
