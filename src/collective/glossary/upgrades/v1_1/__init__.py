# -*- coding: utf-8 -*-
from plone import api
from collective.glossary.logger import logger
from plone.app.textfield.value import RichTextValue


def updateRichtextDefinition(setup_tool):
    """Fill new definition field with old description field."""

    brains = api.content.find(portal_type="Term")
    for brain in brains:
        obj = brain.getObject()
        obj.definition = RichTextValue(
            f"<p>{obj.description}</p>",
            mimeType="text/html",
            outputMimeType="text/html",
        )
        obj.reindexObject()
    logger.info("Fill new definition field with old description field.")
