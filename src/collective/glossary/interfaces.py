# -*- coding: utf-8 -*-
from plone.directives import form
from collective.glossary import _
from zope import schema
from zope.interface import Interface


class IBrowserLayer(Interface):

    """A layer specific for this add-on product."""


class IGlossarySettings(form.Schema):

    """Schema for the control panel form."""

    enable_tooltip = schema.Bool(
        title=_(u'Enable tooltip?'),
        description=_(u'Enable tooltip.'),
        default=True,
    )
