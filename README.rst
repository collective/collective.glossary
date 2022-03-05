.. This README is meant for consumption by humans and pypi. Pypi can render rst files so please do not use Sphinx features.
   If you want to learn more about writing documentation, please check out: http://docs.plone.org/about/documentation_styleguide.html
   This text does not appear on pypi or github. It is a comment.


.. image:: http://img.shields.io/pypi/v/collective.glossary.svg
    :target: https://pypi.python.org/pypi/collective.glossary

.. image:: https://github.com/collective/collective.glossary/actions/workflows/main.yml/badge.svg
    :alt: Github workflow status badge

.. image:: https://img.shields.io/coveralls/collective/collective.glossary/master.svg
    :target: https://coveralls.io/r/collective/collective.glossary


===================
collective.glossary
===================

collective.glossary is a Plone add-on product to define a glossary.

The terms are defined as title / definition pairs. The title can have variants. The definiton is formated richt text.



Translations
------------

This product has been translated into

- german


Installation
------------

Install collective.glossary by adding it to your buildout::

    [buildout]

    ...

    eggs =
        collective.glossary


and then running ``bin/buildout``


Contribute
----------

- Issue Tracker: https://github.com/collective/collective.glossary/issues
- Source Code: https://github.com/collective/collective.glossary
- Documentation: https://docs.plone.org/foo/bar


Support
-------

If you are having issues, please let us know.
We have a mailing list located at: project@example.com


License
-------

The project is licensed under the GPLv2.



Screenshots
-----------

.. figure:: https://raw.github.com/collective/collective.glossary/master/docs/glossary.jpg
    :align: center
    :height: 640px
    :width: 768px

    Create a Glossary.

.. figure:: https://raw.github.com/collective/collective.glossary/master/docs/usage.jpf
    :align: center
    :height: 640px
    :width: 768px

    Use it!

.. figure:: https://raw.github.com/collective/collective.glossary/master/docs/controlpanel.jpg
    :align: center
    :height: 400px
    :width: 768px

    - The tooltip can be disabled in the control panel configlet.
    - Tooltips can be restricted to a selection of content types.

Developer Notes
---------------

The terms are loaded in a page using an AJAX call to a browser view that returns them as a JSON object.

The tooltips will only be available in the default view of a content type instance.
