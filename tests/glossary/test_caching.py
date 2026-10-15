from collective.glossary.api.services.glossary.get import GetGlossaryTerms
from collective.glossary.api.services.glossary.get import GetTooltipTerms
from collective.glossary.setuphandlers import OPERATION_MAPPING
from collective.glossary.setuphandlers import setup_caching
from plone import api
from plone.app.testing import applyProfile
from plone.restapi.testing import RelativeSession
from z3c.caching.registry import lookup

import pytest
import transaction


SMAXAGE = "plone.app.caching.terseCaching.collective.glossary.terms.smaxage"


def install_caching(portal):
    """Install plone.app.caching with a caching proxy, then our rules."""
    applyProfile(portal, "plone.app.caching:default")
    applyProfile(portal, "plone.app.caching:with-caching-proxy")
    setup_caching()
    api.portal.set_registry_record(
        "plone.caching.interfaces.ICacheSettings.enabled", True
    )


@pytest.mark.parametrize("service", [GetGlossaryTerms, GetTooltipTerms])
def test_ruleset(integration, service):
    assert lookup(service()) == "collective.glossary.terms"


def test_setup_caching_without_plone_app_caching(portal):
    """Without plone.app.caching there is nothing to configure."""
    registry = api.portal.get_tool("portal_registry")
    assert OPERATION_MAPPING not in registry.records
    setup_caching()
    assert SMAXAGE not in registry.records


def test_setup_caching(portal):
    install_caching(portal)
    mapping = api.portal.get_registry_record(OPERATION_MAPPING)
    assert mapping["collective.glossary.terms"] == "plone.app.caching.terseCaching"
    # The rulesets of plone.app.caching itself are kept.
    assert mapping["plone.content.dynamic"] == "plone.app.caching.terseCaching"
    assert api.portal.get_registry_record(SMAXAGE) == 300


@pytest.fixture
def anon_session(functional):
    # Anonymous may only use the REST API with its profile.
    applyProfile(functional["portal"], "plone.restapi:default")
    install_caching(functional["portal"])
    transaction.commit()
    session = RelativeSession(functional["portal"].absolute_url())
    session.headers.update({"Accept": "application/json"})
    yield session
    session.close()


def test_tooltip_terms_cache_control(anon_session):
    response = anon_session.get("@tooltip_terms")
    assert response.status_code == 200
    assert response.headers["Cache-Control"] == (
        "max-age=10, s-maxage=300, proxy-revalidate, public"
    )
