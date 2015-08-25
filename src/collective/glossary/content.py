# -*- coding: utf-8 -*-
from collective.glossary.interfaces import IGlossary
from collective.glossary.interfaces import ITerm
from plone.dexterity.content import Container
from plone.dexterity.content import Item
from zope.interface import implements


class Glossary(Container):

    """A Glossary is a container for Terms."""

    implements(IGlossary)


class Term(Item):

    """A Term."""

    implements(ITerm)
