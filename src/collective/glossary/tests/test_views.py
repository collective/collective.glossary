# -*- coding: utf-8 -*-
from collective.glossary.interfaces import IGlossaryLayer
from collective.glossary.testing import INTEGRATION_TESTING
from plone import api
from zope.interface import alsoProvides
from zope.publisher.browser import TestRequest

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
        self.assertEqual(self.view.letters(), [u'F', u'S'])

    def test_terms(self):
        self.assertEqual(
            self.view.terms('F'),
            [{'image': None, 'description': 'First Term Description', 'title': 'First Term'}]
        )
        self.assertEqual(
            self.view.terms('S'),
            [{'image': None, 'description': 'Second Term Description', 'title': 'Second Term'}]
        )


class GlossaryStateViewTestCase(BaseViewTestCase):

    def setUp(self):
        super(GlossaryStateViewTestCase, self).setUp()
        self.view = api.content.get_view(u'glossary_state', self.portal, self.request)

    def test_enable_tooltip(self):
        api.portal.set_registry_record(
            'collective.glossary.interfaces.IGlossarySettings.enable_tooltip',
            True
        )
        self.assertTrue(self.view.enable_tooltip())

        api.portal.set_registry_record(
            'collective.glossary.interfaces.IGlossarySettings.enable_tooltip',
            False
        )
        self.assertFalse(self.view.enable_tooltip())

    def test_is_edit_mode(self):
        self.assertFalse(self.view.is_edit_mode())

        self.view.request = TestRequest(environ={
            'SERVER_URL': 'http://nohost/edit'
        })
        self.assertTrue(self.view.is_edit_mode())

        self.view.request = TestRequest(environ={
            'SERVER_URL': 'http://nohost/anything'
        })
        self.assertFalse(self.view.is_edit_mode())

        self.view.request = TestRequest(environ={
            'SERVER_URL': 'http://nohost/atct_edit'
        })
        self.assertTrue(self.view.is_edit_mode())

    def test_is_glossary_object(self):
        self.assertFalse(self.view.is_glossary_object())

        self.view.request = TestRequest(environ={
            'PARENTS': [self.g1]
        })
        self.assertTrue(self.view.is_glossary_object())

        self.view.request = TestRequest(environ={
            'PARENTS': [self.portal]
        })
        self.assertFalse(self.view.is_glossary_object())

        self.view.request = TestRequest(environ={
            'PARENTS': [self.t1]
        })
        self.assertTrue(self.view.is_glossary_object())


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
