# -*- coding: utf-8 -*-
from collective.glossary.interfaces import IGlossary
from collective.glossary.interfaces import ITerm
from plone.dexterity.content import Container
from plone.dexterity.content import Item
from zope.interface import implementer


@implementer(IGlossary)
class Glossary(Container):

    """A Glossary is a container for Terms."""


@implementer(ITerm)
class Term(Item):

    """A Term."""
