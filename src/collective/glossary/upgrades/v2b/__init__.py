# -*- coding: utf-8 -*-
from collective.glossary.logger import logger
from plone import api


default_profile = "profile-collective.glossary:default"


def updateCatalog(setup):
    setup.runImportStepFromProfile(default_profile, "catalog")
    for brain in api.content.find(portal_type="Term"):
        obj = brain.getObject()
        obj.reindexObject()
    logger.info("Catalog update with index for variants e.a..")
