# -*- coding: utf-8 -*-

from collective.glossary import _
from plone import schema
from plone.app.textfield import RichText
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from Products.CMFPlone.utils import safe_hasattr
from zope.component import adapter
from zope.interface import implementer, Interface, provider


class ITermVariationsMarker(Interface):
    pass


@provider(IFormFieldProvider)
class ITermVariations(model.Schema):
    """ """

    variations = schema.Tuple(
        title=_(u"Variations"),
        description=_(u"Enter the variations of the term, one per line."),
        required=False,
        value_type=schema.TextLine(),
        missing_value=(),
        default=(),
    )

    definition = RichText(
        title=_(u"Definition"),
        description=_(u"Definition of Glossary Term."),
        required=False,
    )


@implementer(ITermVariations)
@adapter(ITermVariationsMarker)
class TermVariations(object):
    def __init__(self, context):
        self.context = context

    @property
    def variations(self):
        if safe_hasattr(self.context, "variations"):
            return self.context.variations
        return None

    @variations.setter
    def variations(self, value):
        self.context.variations = value

    @property
    def definition(self):
        if safe_hasattr(self.context, "definition"):
            return self.context.definition
        return None

    @definition.setter
    def definition(self, value):
        self.context.definition = value
