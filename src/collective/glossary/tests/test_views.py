# -*- coding: utf-8 -*-
from collective.glossary.interfaces import IBrowserLayer
from collective.glossary.testing import INTEGRATION_TESTING
from plone import api
from zope.interface import alsoProvides

import unittest


class BaseViewTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        alsoProvides(self.request, IBrowserLayer)

        with api.env.adopt_roles(['Manager']):
            self.g1 = api.content.create(
                self.portal, 'Glossary', 'g1'
            )
            self.g1.setTitle('Glossary')
            self.g1.setDescription('Glossary Description')
            self.t1 = api.content.create(
                self.g1, 'Term', 't1'
            )
            self.t1.setTitle('First Term')
            self.t1.setDescription('First Term Description')
            self.t2 = api.content.create(
                self.g1, 'Term', 't2'
            )
            self.t2.setTitle('Second Term')
            self.t2.setDescription('Second Term Description')


class TermViewTestCase(BaseViewTestCase):

    def setUp(self):
        super(TermViewTestCase, self).setUp()
        self.view = api.content.get_view(u'view', self.t1, self.request)

    def test_populate(self):
        self.assertEqual(
            self.view.item,
            {'description': 'First Term Description', 'image': None, 'title': 'First Term'}
        )


class GlossaryViewTestCase(BaseViewTestCase):

    def setUp(self):
        super(GlossaryViewTestCase, self).setUp()
        self.view = api.content.get_view(u'view', self.g1, self.request)

    def test_populate(self):
        self.assertEqual()

    def test_letters(self):
        self.assertEqual()

    def test_terms(self):
        self.assertEqual()


class JsonViewTestCase(BaseViewTestCase):

    def setUp(self):
        super(JsonViewTestCase, self).setUp()
        self.view = api.content.get_view(u'glossary', self.portal, self.request)

    def test_populate(self):
        self.assertEqual(
            self.view.data,
            [{'description': '', 'term': ''}, {'description': '', 'term': ''}]
        )
