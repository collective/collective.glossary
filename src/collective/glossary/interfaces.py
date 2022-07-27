# -*- coding: utf-8 -*-
from collective.glossary import _
from collective.glossary.config import DEFAULT_ENABLED_CONTENT_TYPES
from plone.app.textfield import RichText
from plone.autoform import directives as form
from plone.namedfile.field import NamedBlobImage
from plone.supermodel import model
from z3c.form.interfaces import IAddForm, IEditForm
from zope import schema
from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer


class IGlossaryLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


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
        title=_("Text"),
        description=_(""),
        required=False,
    )


class ITerm(Interface):
    """A Term."""

    title = schema.TextLine(
        title=_("Glossary Term"),
        required=True,
    )

    variants = schema.Tuple(
        title=_("Variants"),
        description=_("Enter the variants of the term, one per line."),
        required=False,
        value_type=schema.TextLine(),
        missing_value=(),
        default=(),
    )

    definition = RichText(
        title=_("Definition"),
        description=_("Definition of Glossary Term."),
        required=False,
    )

    image = NamedBlobImage(
        title=_("Image"),
        description=_(""),
        required=False,
    )

    # kick description as comment to settings
    model.fieldset("meta", label=_("Meta"), fields=["description"])
    description = schema.Text(
        title=_("Comment"),
        default="",
        required=False,
    )
    form.omitted("description")
    form.no_omit(IEditForm, "description")
    form.no_omit(IAddForm, "description")
