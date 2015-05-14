# -*- coding: utf-8 -*-
from collective.glossary import _
from plone.directives import form
from plone.namedfile.field import NamedBlobImage
from zope import schema
from zope.interface import Interface


class IGlossaryLayer(Interface):

    """A layer specific for this add-on product."""


class IGlossarySettings(form.Schema):

    """Schema for the control panel form."""

    enable_tooltip = schema.Bool(
        title=_(u'Enable tooltip?'),
        description=_(u'Enable tooltip.'),
        default=True,
    )


class IGlossary(form.Schema):

    """A Glossary is a container for Terms."""


class ITerm(form.Schema):

    """A Term."""

    image = NamedBlobImage(
        title=_(u'Image'),
        description=_(u''),
        required=False,
    )
