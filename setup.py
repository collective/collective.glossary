# -*- coding: utf-8 -*-
"""Installer for the collective.glossary package."""

from setuptools import find_packages, setup


long_description = "\n\n".join(
    [
        open("README.rst").read(),
        open("CONTRIBUTORS.rst").read(),
        open("CHANGES.rst").read(),
    ]
)

setup(
    name="collective.glossary",
    version="2.0.3",
    description="Content types to define a glossary and its terms",
    long_description=long_description,
    # Get more from https://pypi.org/classifiers/
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: Addon",
        "Framework :: Plone :: 5.2",
        "Framework :: Plone :: 6.0",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
    ],
    keywords="Python Plone CMS",
    author="Simples Consultoria",
    author_email="products@simplesconsultoria.com.br",
    url="https://github.com/collective/collective.glossary",
    project_urls={
        "PyPI": "https://pypi.python.org/pypi/collective.glossary",
        "Source": "https://github.com/collective/collective.glossary",
        "Tracker": "https://github.com/collective/collective.glossary/issues",
        # 'Documentation': 'https://collective.glossary.readthedocs.io/en/latest/',
    },
    license="GPL version 2",
    packages=find_packages("src", exclude=["ez_setup"]),
    namespace_packages=["collective"],
    package_dir={"": "src"},
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.7",
    install_requires=[
        "setuptools",
        # -*- Extra requirements: -*-
        "z3c.jbot",
        "plone.api>=1.8.4",
        "plone.restapi",
        "plone.app.dexterity",
    ],
    extras_require={
        "test": [
            # "plone.app.testing",
            "plone.testing>=5.0.0",
            "plone.app.contenttypes",
            # "plone.app.robotframework[debug]",
            # how easyform does it:
            "plone.app.testing[robot]",
            "plone.app.robotframework",
            # "plone.app.contenttypes",
            "robotframework-selenium2library",
            "robotframework-selenium2screenshots",
        ],
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    [console_scripts]
    update_locale = collective.glossary.locales.update:update_locale
    """,
)
