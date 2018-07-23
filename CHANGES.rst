Changelog
=========

1.0b2 (unreleased)
------------------

- Add HTTP caching headers to ``@@glossary`` view (fixes `#24 <https://github.com/collective/collective.glossary/issues/24>`_).
  [hvelarde]

- Code clean up to remove useless memoizer and reduce memory consumption (closes `#37 <https://github.com/collective/collective.glossary/issues/37>`_).
  [hvelarde]

- Drop support for Plone 5.0.
  [hvelarde]


1.0b1 (2016-12-19)
------------------

- Term template was refactored to avoid duplicated definitions (closes `#26`_)
  [hvelarde]

- Glossary terms now use ``tile`` scales (closes `#5`_).
  [hvelarde]

- Remove dependency on five.grok.
  [hvelarde]

- Fix ``ReferenceError`` on JavaScript code (Plone 5 does not include global variables anymore).
  [hvelarde, rodfersou]

- Remove dependency on Products.CMFQuickInstallerTool.
  [hvelarde]

- Change glossary to always call JSON view from the portal URL (closes `#22`).
  [rodfersou]

- A new rich text field was added to the Glossary content type.
  [hvelarde]

- Normalize glossary index (closes `#18`_).
  [rodfersou]

- Add option to select content types that will display glossary terms (closes `#14`_).
  [rodfersou]

- Apply Glossary just to #content-core. (closes `#12`_).
  [rodfersou]

- Review method `is_view_action` to work with Virtual Host configuration.
  [rodfersou]

- Terms should only be added inside a Glossary (closes `#8`_).
  [hvelarde]


1.0a1 (2015-05-18)
------------------

- Initial release.

.. _`#5`: https://github.com/collective/collective.cover/issues/5
.. _`#8`: https://github.com/collective/collective.cover/issues/8
.. _`#12`: https://github.com/collective/collective.cover/issues/12
.. _`#14`: https://github.com/collective/collective.cover/issues/14
.. _`#18`: https://github.com/collective/collective.cover/issues/18
.. _`#22`: https://github.com/collective/collective.cover/issues/22
.. _`#26`: https://github.com/collective/collective.cover/issues/26
