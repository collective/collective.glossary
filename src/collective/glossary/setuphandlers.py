from plone import api
from Products.CMFPlone.interfaces import INonInstallable
from zope.interface import implementer


CACHING_PROFILE = "profile-collective.glossary:caching"
OPERATION_MAPPING = "plone.caching.interfaces.ICacheSettings.operationMapping"


@implementer(INonInstallable)
class HiddenProfiles:  # pragma: no cover
    @staticmethod
    def getNonInstallableProfiles():
        """Do not show on Plone's list of installable profiles."""
        return [
            "collective.glossary:caching",
            "collective.glossary:uninstall",
        ]


def setup_caching(context=None):
    """Apply the caching profile when plone.app.caching is installed.

    Without plone.app.caching the caching rules have nothing to configure,
    and the profile cannot be applied.
    """
    registry = api.portal.get_tool("portal_registry")
    if OPERATION_MAPPING not in registry.records:
        return
    setup = api.portal.get_tool("portal_setup")
    setup.runAllImportStepsFromProfile(CACHING_PROFILE, dependency_strategy="ignore")


def post_install(context):
    """Post install script."""
    setup_caching()
