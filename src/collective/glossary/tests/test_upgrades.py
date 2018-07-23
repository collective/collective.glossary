# -*- coding: utf-8 -*-
from collective.glossary.testing import INTEGRATION_TESTING
from collective.glossary.testing import IS_PLONE_5
from plone import api

import unittest


class UpgradeTestCaseBase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self, from_version, to_version):
        self.portal = self.layer['portal']
        self.setup = self.portal['portal_setup']
        self.profile_id = u'collective.glossary:default'
        self.from_version = from_version
        self.to_version = to_version

    def get_upgrade_step(self, title):
        """Get the named upgrade step."""
        self.setup.setLastVersionForProfile(self.profile_id, self.from_version)
        upgrades = self.setup.listUpgrades(self.profile_id)
        steps = [s for s in upgrades[0] if s['title'] == title]
        return steps[0] if steps else None

    def execute_upgrade_step(self, step):
        """Execute an upgrade step."""
        request = self.layer['request']
        request.form['profile_id'] = self.profile_id
        request.form['upgrades'] = [step['id']]
        self.setup.manage_doUpgrades(request=request)

    @property
    def total_steps(self):
        """Return the number of steps in the upgrade."""
        self.setup.setLastVersionForProfile(self.profile_id, self.from_version)
        upgrades = self.setup.listUpgrades(self.profile_id)
        assert len(upgrades) > 0
        return len(upgrades[0])


class Upgrade1to2TestCase(UpgradeTestCaseBase):

    def setUp(self):
        UpgradeTestCaseBase.setUp(self, u'1', u'2')

    def test_upgrade_to_2_registrations(self):
        version = self.setup.getLastVersionForProfile(self.profile_id)[0]
        self.assertGreaterEqual(int(version), int(self.to_version))
        self.assertEqual(self.total_steps, 4)

    @unittest.skipIf(IS_PLONE_5, 'Upgrade step not supported under Plone 5')
    def test_update_resource_conditions(self):
        # check if the upgrade step is registered
        title = u'Update resource conditions'
        step = self.get_upgrade_step(title)
        self.assertIsNotNone(step)

        js_tool = api.portal.get_tool('portal_javascripts')
        JS_IDS = (
            '++resource++collective.glossary/tooltip.js',
            '++resource++collective.glossary/jquery.glossarize.js',
            '++resource++collective.glossary/main.js',
        )
        css_tool = api.portal.get_tool('portal_css')
        CSS_IDS = ('++resource++collective.glossary/tooltip.css',)

        # simulate state on previous version
        for id_ in JS_IDS:
            js = js_tool.getResource(id_)
            js.setExpression("python:portal.restrictedTraverse('@@glossary_state')()")
        for id_ in CSS_IDS:
            css = css_tool.getResource(id_)
            css.setExpression("python:portal.restrictedTraverse('@@glossary_state')()")

        # run the upgrade step to validate the update
        self.execute_upgrade_step(step)

        # Check expected expression
        for id_ in JS_IDS:
            js = js_tool.getResource(id_)
            self.assertEqual(js.getExpression(), 'context/@@glossary_state')
        for id_ in CSS_IDS:
            css = css_tool.getResource(id_)
            self.assertEqual(css.getExpression(), 'context/@@glossary_state')
