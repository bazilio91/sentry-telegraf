#!/usr/bin/env python
from setuptools import setup

import sentry_telegraf

install_requires = [
    'pytelegraf',
]

f = open('README.rst')
readme = f.read()
f.close()

setup(
    name='sentry-telegraf',
    version=sentry_telegraf.__version__,
    author='Vasiliy Ostanin',
    author_email='bazilio91@gmail.com',
    url='http://github.com/bazilio91/sentry-telegraf',
    description='A Sentry extension which send errors stats to telegraf',
    long_description=readme,
    license='MIT',
    packages=['sentry_telegraf'],
    install_requires=install_requires,
    entry_points={
        'sentry.plugins': [
            'sentry_telegraf = sentry_telegraf.plugin:TelegrafPlugin'
        ],
    },
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Software Development'
    ],
    keywords='sentry telegraf',
)
