# -*- coding: utf-8 -*-
from collective.glossary.config import PROJECTNAME
from collective.glossary.logger import logger
from plone import api


def update_resource_conditions(setup_tool):
    """Update resource conditions."""
    profile = "profile-{0}:default".format(PROJECTNAME)
    setup_tool.runImportStepFromProfile(profile, "cssregistry")
    setup_tool.runImportStepFromProfile(profile, "jsregistry")
    logger.info("Conditions to include package resources were updated.")


def update_controlpanel_options(setup_tool):
    """Update control panel options."""
    profile = "profile-{0}:default".format(PROJECTNAME)
    setup_tool.runImportStepFromProfile(profile, "plone.app.registry")
    logger.info("Added option to select the content type to use glossary.")


def cook_css_resources(context):  # pragma: no cover
    """Cook css resources."""
    css_tool = api.portal.get_tool("portal_css")
    css_tool.cookResources()
    logger.info("CSS resources were cooked")


def cook_javascript_resources(context):  # pragma: no cover
    """Cook JavaScript resources."""
    js_tool = api.portal.get_tool("portal_javascripts")
    js_tool.cookResources()
    logger.info("JavaScript resources were cooked")
