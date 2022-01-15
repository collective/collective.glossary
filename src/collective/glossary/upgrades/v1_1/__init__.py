# -*- coding: utf-8 -*-
from plone import api
from collective.glossary.logger import logger
from plone.app.textfield.value import RichTextValue


def updateRichtextDefinition(setup_tool):
    """Fill new definition field with old description field."""

    brains = api.content.find(portal_type="Term")
    for brain in brains:
        obj = brain.getObject()
        if not obj.definition:
            obj.definition = RichTextValue(
                f"<p>{obj.description}</p>",
                mimeType="text/html",
                outputMimeType="text/html",
            )
        else:
            logger.info("found term definition. Do not overwrite. " + obj.definition.raw)
        obj.reindexObject()
    logger.info("Fill new definition field with old description field.")
