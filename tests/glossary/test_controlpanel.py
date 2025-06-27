import pytest
from collective.glossary.controlpanel import IGlossarySettings
from collective.glossary.interfaces import IBrowserLayer
from plone import api
from plone.app.testing import logout
from plone.registry.interfaces import IRegistry
from zope.component import getUtility
from zope.interface import alsoProvides


class TestControlPanel:
    def test_controlpanel_has_view(self, portal, request):
        alsoProvides(request, IBrowserLayer)
        view = api.content.get_view(name="glossary-settings", context=portal)
        assert view()

    def test_controlpanel_view_is_protected(self, portal):
        from AccessControl import Unauthorized

        logout()
        with pytest.raises(Unauthorized):
            portal.restrictedTraverse("@@glossary-settings")

    def test_controlpanel_installed(self, portal):
        controlpanel = portal["portal_controlpanel"]
        actions = [a.getAction(controlpanel)["id"] for a in controlpanel.listActions()]
        assert "glossary" in actions


class TestRegistry:
    def test_enable_tooltip_record_in_registry(self, portal):
        registry = getUtility(IRegistry)
        settings = registry.forInterface(IGlossarySettings)
        assert hasattr(settings, "enable_tooltip")
        assert settings.enable_tooltip is True

    def test_enabled_content_types_record_in_registry(self, portal):
        from collective.glossary.config import DEFAULT_ENABLED_CONTENT_TYPES

        registry = getUtility(IRegistry)
        settings = registry.forInterface(IGlossarySettings)
        assert hasattr(settings, "enabled_content_types")
        assert settings.enabled_content_types == DEFAULT_ENABLED_CONTENT_TYPES
