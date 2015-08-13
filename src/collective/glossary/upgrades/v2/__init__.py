# -*- coding: utf-8 -*-
from collective.glossary.config import PROJECTNAME
from collective.glossary.logger import logger


def update_resource_conditions(setup_tool):
    """Update resource conditions."""
    profile = 'profile-{0}:default'.format(PROJECTNAME)
    setup_tool.runImportStepFromProfile(profile, 'cssregistry')
    setup_tool.runImportStepFromProfile(profile, 'jsregistry')
    logger.info('Conditions to include package resources were updated.')
