# -*- coding: utf-8 -*-
from plone import api
from plone.app.testing import (
    FunctionalTesting,
    IntegrationTesting,
    PLONE_FIXTURE,
    PloneSandboxLayer,
)


IS_PLONE_5 = api.env.plone_version().startswith("5")


class Fixture(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        import collective.glossary

        self.loadZCML(package=collective.glossary)

    def setUpPloneSite(self, portal):
        self.applyProfile(portal, "collective.glossary:default")


FIXTURE = Fixture()

INTEGRATION_TESTING = IntegrationTesting(
    bases=(FIXTURE,), name="collective.glossary:Integration"
)

FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FIXTURE,), name="collective.glossary:Functional"
)
