# -*- coding: utf-8 -*-
from collective.glossary.interfaces import ITerm
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

        self.t1 = api.content.create(self.g1, "Term", "t1")

    def test_adding(self):
        self.assertTrue(ITerm.providedBy(self.t1))

    def test_adding_outside_glossary(self):
        from plone.api.exc import InvalidParameterError

        with self.assertRaises(InvalidParameterError):
            api.content.create(self.portal, "Term", "test")

    def test_fti(self):
        fti = queryUtility(IDexterityFTI, name="Term")
        self.assertIsNotNone(fti)

    def test_schema(self):
        fti = queryUtility(IDexterityFTI, name="Term")
        schema = fti.lookupSchema()
        self.assertEqual(ITerm, schema)

    def test_factory(self):
        fti = queryUtility(IDexterityFTI, name="Term")
        factory = fti.factory
        new_object = createObject(factory)
        self.assertTrue(ITerm.providedBy(new_object))
