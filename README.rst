.. This README is meant for consumption by humans and pypi. Pypi can render rst files so please do not use Sphinx features.
   If you want to learn more about writing documentation, please check out: http://docs.plone.org/about/documentation_styleguide.html
   This text does not appear on pypi or github. It is a comment.


.. image:: http://img.shields.io/pypi/v/collective.glossary.svg
    :target: https://pypi.python.org/pypi/collective.glossary

.. image:: https://github.com/collective/collective.glossary/actions/workflows/main.yml/badge.svg
    :alt: Github workflow status badge


===================
collective.glossary
===================

**collective.glossary** is a Plone backend add-on to define a glossary and provide tooltips on matching text.

- The terms are defined as title / definition pairs.
- The term can have variants.
- The definiton is richtext formated.
- The tooltip can be disabled in glossary control panel.
- Tooltips can be restricted to a selection of content types.

The add-on provides a REST API service @glossary_terms to fetch the terms of the glossary.

`@rohberg/volto-slate-glossary <https://github.com/rohberg/volto-slate-glossary>`_ is the corresponding Volto add-on.



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

If you are having issues, please let us know: `community.plone.org <https://community.plone.org/>`_


License
-------

The project is licensed under the GPLv2.



Screenshots
-----------

.. figure:: https://raw.github.com/collective/collective.glossary/master/docs/glossary.png
    :align: left

    Create a Glossary.

.. figure:: https://raw.github.com/collective/collective.glossary/master/docs/usage.png
    :align: left

    Use it!

.. figure:: https://raw.github.com/collective/collective.glossary/master/docs/controlpanel.png
    :align: left
