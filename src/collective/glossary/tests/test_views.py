# -*- coding: utf-8 -*-
from collective.glossary.interfaces import IGlossarySettings
from collective.glossary.testing import INTEGRATION_TESTING
from plone import api
from plone.app.textfield.value import RichTextValue
from zope.publisher.browser import TestRequest

import unittest


class BaseViewTestCase(unittest.TestCase):
    layer = INTEGRATION_TESTING

    def setUp(self):
        self.app = self.layer["app"]
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]

        with api.env.adopt_roles(["Manager"]):
            self.g1 = api.content.create(
                self.portal,
                "Glossary",
                "g1",
                title="Glossary",
                definition=RichTextValue(
                    "<p>Glossary Description</p>",
                    mimeType="text/html",
                    outputMimeType="text/html",
                ),
            )
            self.t1 = api.content.create(
                self.g1,
                "Term",
                "t1",
                title="First Term",
                variants=["FTD", "MFTD"],
                definition=RichTextValue(
                    "<p>First Term Description</p>",
                    mimeType="text/html",
                    outputMimeType="text/html",
                ),
            )
            self.t2 = api.content.create(
                self.g1,
                "Term",
                "t2",
                title="Second Term",
                variants=["STD", "MSTD"],
                definition=RichTextValue(
                    "<p>Second Term Description</p>",
                    mimeType="text/html",
                    outputMimeType="text/html",
                ),
            )
            self.d1 = api.content.create(
                self.portal,
                "Document",
                "d1",
                title="Document",
                definition=RichTextValue(
                    "<p>Document Description</p>",
                    mimeType="text/html",
                    outputMimeType="text/html",
                ),
            )


class GlossaryViewTestCase(BaseViewTestCase):
    def setUp(self):
        super(GlossaryViewTestCase, self).setUp()
        self.view = api.content.get_view("view", self.g1, self.request)

    def test_get_entries(self):
        expected = {
            "F": [
                {
                    "image": None,
                    "definition": "<p>First Term Description</p>",
                    "variants": ["FTD", "MFTD"],
                    "title": "First Term",
                    "url": "http://nohost/plone/g1/t1",
                    "state": "private",
                }
            ],
            "S": [
                {
                    "image": None,
                    "definition": "<p>Second Term Description</p>",
                    "variants": ["STD", "MSTD"],
                    "title": "Second Term",
                    "url": "http://nohost/plone/g1/t2",
                    "state": "private",
                }
            ],
        }
        self.assertEqual(dict(self.view.get_entries()), expected)

    def test_letters(self):
        self.assertEqual(self.view.letters(), ["F", "S"])

    def test_terms(self):
        expected = [
            {
                "title": "First Term",
                "definition": "<p>First Term Description</p>",
                "variants": ["FTD", "MFTD"],
                "state": "private",
                "url": "http://nohost/plone/g1/t1",
                "image": None,
            }
        ]
        self.assertEqual(self.view.terms("F"), expected)

        expected = [
            {
                "title": "Second Term",
                "definition": "<p>Second Term Description</p>",
                "variants": ["STD", "MSTD"],
                "state": "private",
                "url": "http://nohost/plone/g1/t2",
                "image": None,
            }
        ]
        self.assertEqual(self.view.terms("S"), expected)


class GlossaryStateViewTestCase(BaseViewTestCase):
    def setUp(self):
        super(GlossaryStateViewTestCase, self).setUp()
        self.view = api.content.get_view("glossary_state", self.portal, self.request)

    def test_tooltip_is_enabled(self):
        name = IGlossarySettings.__identifier__ + ".enable_tooltip"
        api.portal.set_registry_record(name, True)
        self.assertTrue(self.view.tooltip_is_enabled)

        name = IGlossarySettings.__identifier__ + ".enable_tooltip"
        api.portal.set_registry_record(name, False)
        self.assertFalse(self.view.tooltip_is_enabled)

    def test_content_type_is_enabled(self):
        self.assertFalse(self.view.content_type_is_enabled)

        self.view.context = self.d1
        self.assertTrue(self.view.content_type_is_enabled)

        self.view.context = self.g1
        self.assertFalse(self.view.content_type_is_enabled)

    def test_is_view_action(self):
        self.assertTrue(self.view.is_view_action)

        self.view.request = TestRequest(
            environ={
                "SERVER_URL": "http://nohost",
                "PATH_INFO": "/folder_contents",
            }
        )
        self.view.request.base = "http://nohost/plone"
        self.assertFalse(self.view.is_view_action)

        self.view.context = self.g1
        self.view.request = TestRequest(
            environ={
                "SERVER_URL": "http://nohost/plone/g1",
                "PATH_INFO": "/g1",
            }
        )
        self.view.request.base = "http://nohost/plone"
        self.assertTrue(self.view.is_view_action)

        self.view.request = TestRequest(
            environ={
                "SERVER_URL": "http://nohost/plone/g1",
                "PATH_INFO": "/g1/edit",
            }
        )
        self.view.request.base = "http://nohost/plone"
        self.assertFalse(self.view.is_view_action)


class JsonViewTestCase(BaseViewTestCase):
    def setUp(self):
        super(JsonViewTestCase, self).setUp()
        self.view = api.content.get_view("glossary", self.portal, self.request)

    def test_get_json_entries(self):
        expected = [
            {"term": "FTD", "description": "<p>First Term Description</p>"},
            {"term": "First Term", "description": "<p>First Term Description</p>"},
            {"term": "MFTD", "description": "<p>First Term Description</p>"},
            {"term": "MSTD", "description": "<p>Second Term Description</p>"},
            {"term": "STD", "description": "<p>Second Term Description</p>"},
            {"term": "Second Term", "description": "<p>Second Term Description</p>"},
        ]
        self.assertEqual(self.view.get_json_entries(), expected)

    def test__call__(self):
        import json

        self.view()
        result = self.view.request.response.getBody()

        expected = [
            {"term": "FTD", "description": "<p>First Term Description</p>"},
            {"term": "First Term", "description": "<p>First Term Description</p>"},
            {"term": "MFTD", "description": "<p>First Term Description</p>"},
            {"term": "MSTD", "description": "<p>Second Term Description</p>"},
            {"term": "STD", "description": "<p>Second Term Description</p>"},
            {"term": "Second Term", "description": "<p>Second Term Description</p>"},
        ]
        self.assertEqual(json.loads(result), expected)
