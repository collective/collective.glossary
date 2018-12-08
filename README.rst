********
Glossary
********

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

Known issues
------------

See the `complete list of bugs on GitHub <https://github.com/collective/collective.glossary/labels/bug>`_.

Don't Panic
===========

Installation
------------

To enable this package in a buildout-based installation:

#. Edit your buildout.cfg and add ``collective.glossary`` to the list of eggs to install:

.. code-block:: ini

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


How does it work
----------------

The terms are loaded in a page using an AJAX call to a browser view that returns them as a JSON object.

The tooltips will only be available in the default view of a content type instance.


Look Ma! No Resource Registries
-------------------------------
This add-on uses a very opinionated approach on how to handle static resources in Plone.
We just deprecated resource registries in favor of a simpler approach: a viewlet in ``plone.htmlhead``.
This simplifies maintainance among multiple Plone versions and avoids bundling of unrelated resources.


Development
-----------

We use `webpack <https://webpack.js.org/>`_ to process static resources on this package.
`webpack`_ processes SCSS and JS files, minifies the resulting CSS and JS, and optimizes all images.

To contribute, you should start the instance in one shell and start webpack watcher on another with the following command:

.. code-block:: console

    $ bin/watch-glossary

Then go to ``webpack/app`` folder and edit SCSS and JS files;
`webpack`_ watcher will automatically create the final resources in the right place.

There are also other commands added to handle more complex scenarios.

The following command will set the buildout node installation in the system PATH,
this way you can use `webpack`_ as described on their documentation.

.. code-block:: console

    $ bin/env-glossary

The following command generates JS and CSS without the minify step (it can be used to check the code being generated in a human readable way).

.. code-block:: console

    $ bin/debug-glossary

The following command rebuilds static files and exit (insted of keep watching the changes):

.. code-block:: console

    $ bin/build-glossary
