# -*- coding: utf-8 -*-
from collective.glossary.logger import logger
from plone import api
from plone.app.textfield.value import RichTextValue


def updateRichtextDefinition(setup_tool):
    """Fill new definition field with old description field."""

    logger.info("Fill new definition field with old description field.")

    brains = api.content.find(portal_type="Term")
    for brain in brains:
        obj = brain.getObject()
        if not obj.definition:
            logger.info("Intitialize " + obj.id + " " + obj.description)
            obj.definition = RichTextValue(
                f"<p>{obj.description}</p>",
                mimeType="text/html",
                outputMimeType="text/html",
            )
            obj.description = ""
        else:
            logger.info(
                "Found term definition for "
                + obj.id
                + ". Do not overwrite. "
                + obj.definition.raw
            )
        obj.reindexObject()
    logger.info("Glossary term definitions initialized.")
