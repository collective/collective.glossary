***************
Glossary
***************

.. contents:: Table of Contents

Life, the Universe, and Everything
==================================

A Dexterity-based content type to define a glossary and its terms.

This package is inspired in `PloneGlossary`_.

.. _`PloneGlossary`: https://pypi.python.org/pypi/Products.PloneGlossary

Mostly Harmless
===============

.. image:: http://img.shields.io/pypi/v/collective.glossary.svg
    :target: https://pypi.python.org/pypi/collective.glossary

.. image:: https://img.shields.io/travis/collective/collective.glossary/master.svg
    :target: http://travis-ci.org/collective/collective.glossary

.. image:: https://img.shields.io/coveralls/collective/collective.glossary/master.svg
    :target: https://coveralls.io/r/collective/collective.glossary

Got an idea? Found a bug? Let us know by `opening a support ticket`_.

.. _`opening a support ticket`: https://github.com/collective/collective.glossary/issues

Don't Panic
===========

Installation
------------

To enable this package in a buildout-based installation:

#. Edit your buildout.cfg and add add the following to it::

    [buildout]
    ...
    eggs =
        collective.glossary

After updating the configuration you need to run ''bin/buildout'', which will take care of updating your system.

Go to the 'Site Setup' page in a Plone site and click on the 'Add-ons' link.

Check the box next to ``collective.glossary`` and click the 'Activate' button.

Usage
-----

TBD.


Screenshots
-----------

.. figure:: https://raw.github.com/collective/collective.glossary/master/docs/glossary.png
    :align: center
    :height: 640px
    :width: 768px

    Create a Glossary.

.. figure:: https://raw.github.com/collective/collective.glossary/master/docs/usage.png
    :align: center
    :height: 640px
    :width: 768px

    Use it!

.. figure:: https://raw.github.com/collective/collective.glossary/master/docs/controlpanel.png
    :align: center
    :height: 400px
    :width: 768px

    The tooltip can be disabled in the control panel configlet.

Developer Notes
---------------

The terms are loaded in a page using an AJAX call to a browser view that returns them as a JSON object.

The tooltips will only be available in the default view of a content type instance.
