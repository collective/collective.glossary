# -*- coding: utf-8 -*-
from setuptools import find_packages
from setuptools import setup

version = '1.1b1.dev0'
description = 'A Dexterity-based content type to define a glossary and its terms.'
long_description = (
    open('README.rst').read() + '\n' +
    open('CONTRIBUTORS.rst').read() + '\n' +
    open('CHANGES.rst').read()
)

setup(
    name='collective.glossary',
    version=version,
    description=description,
    long_description=long_description,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Plone',
        'Framework :: Plone :: 4.3',
        'Framework :: Plone :: 5.1',
        'Intended Audience :: Education',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords='plone glossary',
    author='Simples Consultoria',
    author_email='products@simplesconsultoria.com.br',
    url='https://github.com/collective/collective.glossary',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['collective'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'plone.api',
        'plone.app.dexterity',
        'plone.app.registry',
        'plone.dexterity',
        'plone.namedfile',
        'Products.CMFPlone >=4.3',
        'Products.GenericSetup',
        'setuptools',
        'zope.globalrequest',
        'zope.i18nmessageid',
        'zope.interface',
        'zope.schema',
        'zope.ucol'
    ],
    extras_require={
        'test': [
            'AccessControl',
            'plone.app.robotframework',
            'plone.app.testing [robot]',
            'plone.browserlayer',
            'plone.registry',
            'plone.testing',
            'robotsuite',
            'zope.component',
        ],
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
