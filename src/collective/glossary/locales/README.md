# Adding and updating locales

For every language you want to translate into you need a
locales/[language]/LC_MESSAGES/collective.glossary.po
(e.g. locales/it/LC_MESSAGES/collective.glossary.po)

For italian

    mkdir -p it/LC_MESSAGES/
    touch it/LC_MESSAGES/collective.glossary.po

For updating locales

    cd src/collective/glossary/locales
    ./update.sh

Install i18ndude via pip if not already installed.


Note
----

The script uses gettext package for internationalization.

Install it before running the script.


On macOS
--------

.. code-block:: console

    $ brew install gettext

On Windows
----------

see https://mlocati.github.io/articles/gettext-iconv-windows.html
