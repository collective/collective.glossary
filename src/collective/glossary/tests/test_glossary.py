# -*- coding: utf-8 -*-
from collective.glossary.interfaces import IGlossary
from collective.glossary.testing import INTEGRATION_TESTING
from plone import api
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import createObject, queryUtility

import unittest


class GlossaryTypeTestCase(unittest.TestCase):
    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]

        with api.env.adopt_roles(["Manager"]):
            self.g1 = api.content.create(self.portal, "Glossary", "g1")

    def test_adding(self):
        self.assertTrue(IGlossary.providedBy(self.g1))

    def test_fti(self):
        fti = queryUtility(IDexterityFTI, name="Glossary")
        self.assertIsNotNone(fti)

    def test_schema(self):
        fti = queryUtility(IDexterityFTI, name="Glossary")
        schema = fti.lookupSchema()
        self.assertEqual(IGlossary, schema)

    def test_factory(self):
        fti = queryUtility(IDexterityFTI, name="Glossary")
        factory = fti.factory
        new_object = createObject(factory)
        self.assertTrue(IGlossary.providedBy(new_object))

    def test_is_selectable_as_folder_default_view(self):
        self.portal.setDefaultPage("g1")
        self.assertEqual(self.portal.default_page, "g1")

    def test_not_allowed_content_types(self):
        from plone.api.exc import InvalidParameterError

        with self.assertRaises(InvalidParameterError):
            api.content.create(self.g1, "Document", "test")
