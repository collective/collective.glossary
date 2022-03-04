# -*- coding: utf-8 -*-
from collective.glossary.interfaces import IGlossary, ITerm
from plone.dexterity.content import Container, Item
from zope.interface import implementer


@implementer(IGlossary)
class Glossary(Container):

    """A Glossary is a container for Terms."""


@implementer(ITerm)
class Term(Item):

    """A Term."""
