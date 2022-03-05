# -*- coding: utf-8 -*-
from collective.glossary import _
from collective.glossary.config import DEFAULT_ENABLED_CONTENT_TYPES
from plone.app.textfield import RichText
from plone.namedfile.field import NamedBlobImage
from zope import schema
from zope.interface import Interface


class IGlossaryLayer(Interface):

    """A layer specific for this add-on product."""


class IGlossarySettings(Interface):

    """Schema for the control panel form."""

    enable_tooltip = schema.Bool(
        title=_("Enable tooltip?"),
        description=_("Enable tooltip."),
        default=True,
    )

    enabled_content_types = schema.List(
        title=_("Enabled Content Types"),
        description=_(
            "Only objects of these content types will display glossary terms."
        ),
        required=False,
        default=DEFAULT_ENABLED_CONTENT_TYPES,
        # we are going to list only the main content types in the widget
        value_type=schema.Choice(vocabulary="collective.glossary.PortalTypes"),
    )


class IGlossary(Interface):

    """A Glossary is a container for Terms."""

    text = RichText(
        title=_("Body text"),
        description=_(""),
        required=False,
    )


class ITerm(Interface):

    """A Term."""

    # default fieldset

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

    image = NamedBlobImage(
        title=_("Image"),
        description=_(""),
        required=False,
    )

    # TODO description of description
