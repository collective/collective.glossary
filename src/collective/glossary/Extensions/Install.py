from collective.glossary.config import PROJECTNAME
from plone import api


def uninstall(portal, reinstall=False):
    if not reinstall:
        profile = f"profile-{PROJECTNAME}:uninstall"
        setup_tool = api.portal.get_tool("portal_setup")
        setup_tool.runAllImportStepsFromProfile(profile)
        return "Ran all uninstall steps."
