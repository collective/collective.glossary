# -*- coding: utf-8 -*-
from collective.glossary.behaviors.term_variations import ITermVariationsMarker
from collective.glossary.testing import INTEGRATION_TESTING  # noqa
from plone.app.testing import setRoles, TEST_USER_ID
from plone.behavior.interfaces import IBehavior
from zope.component import getUtility

import unittest


class TermVariationsIntegrationTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_behavior_term_variations(self):
        behavior = getUtility(IBehavior, 'collective.glossary.term_variations')
        self.assertEqual(
            behavior.marker,
            ITermVariationsMarker,
        )
