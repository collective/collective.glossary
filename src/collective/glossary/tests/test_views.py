# -*- coding: utf-8 -*-
from collective.glossary.interfaces import IGlossaryLayer
from collective.glossary.testing import INTEGRATION_TESTING
from plone import api
from zope.interface import alsoProvides

import unittest


class BaseViewTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        alsoProvides(self.request, IGlossaryLayer)

        with api.env.adopt_roles(['Manager']):
            self.g1 = api.content.create(
                self.portal, 'Glossary', 'g1',
                title='Glossary',
                description='Glossary Description'
            )
            self.t1 = api.content.create(
                self.g1, 'Term', 't1',
                title='First Term',
                description='First Term Description'
            )
            self.t2 = api.content.create(
                self.g1, 'Term', 't2',
                title='Second Term',
                description='Second Term Description'
            )


class TermViewTestCase(BaseViewTestCase):

    def setUp(self):
        super(TermViewTestCase, self).setUp()
        self.view = api.content.get_view(u'view', self.t1, self.request)

    def test_prepare_item(self):
        self.assertEqual(
            self.view.prepare_item(),
            {'description': 'First Term Description', 'image': None, 'title': 'First Term'}
        )


class GlossaryViewTestCase(BaseViewTestCase):

    def setUp(self):
        super(GlossaryViewTestCase, self).setUp()
        self.view = api.content.get_view(u'view', self.g1, self.request)

    def test_prepare_items(self):
        self.assertEqual(
            self.view.prepare_items(),
            {
                'F': [{
                    'image': None,
                    'description': 'First Term Description',
                    'title': 'First Term'
                }],
                'S': [{
                    'image': None,
                    'description': 'Second Term Description',
                    'title': 'Second Term'
                }]
            }
        )

    def test_letters(self):
        self.assertEqual(self.view.letters(), {'F', 'S'})

    def test_terms(self):
        self.assertEqual(
            self.view.terms('F'),
            [{'image': None, 'description': 'First Term Description', 'title': 'First Term'}]
        )
        self.assertEqual(
            self.view.terms('S'),
            [{'image': None, 'description': 'Second Term Description', 'title': 'Second Term'}]
        )


class JsonViewTestCase(BaseViewTestCase):

    def setUp(self):
        super(JsonViewTestCase, self).setUp()
        self.view = api.content.get_view(u'glossary', self.portal, self.request)

    def test_get_items(self):
        self.assertEqual(
            self.view.prepare_items(),
            [{'description': 'First Term Description', 'term': 'First Term'},
             {'description': 'Second Term Description', 'term': 'Second Term'}]
        )
