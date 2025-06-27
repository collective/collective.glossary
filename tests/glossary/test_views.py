import json
import pytest
from collective.glossary.interfaces import IGlossarySettings
from plone import api
from plone.app.textfield.value import RichTextValue


@pytest.fixture
def glossary_content(portal):
    """Create glossary content for tests."""
    with api.env.adopt_roles(["Manager"]):
        g1 = api.content.create(
            portal,
            "Glossary",
            "g1",
            title="Glossary",
            definition=RichTextValue(
                "<p>Glossary Description</p>",
                mimeType="text/html",
                outputMimeType="text/html",
            ),
        )
        t1 = api.content.create(
            g1,
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
        t2 = api.content.create(
            g1,
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
        d1 = api.content.create(
            portal,
            "Document",
            "d1",
            title="Document",
            definition=RichTextValue(
                "<p>Document Description</p>",
                mimeType="text/html",
                outputMimeType="text/html",
            ),
        )

    return {
        "glossary": g1,
        "term1": t1,
        "term2": t2,
        "document": d1,
    }


class TestGlossaryView:
    @pytest.fixture(autouse=True)
    def setup_view(self, portal, request, glossary_content):
        self.g1 = glossary_content["glossary"]
        self.t1 = glossary_content["term1"]
        self.t2 = glossary_content["term2"]
        self.d1 = glossary_content["document"]
        self.view = api.content.get_view(name="view", context=self.g1)

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
        assert dict(self.view.get_entries()) == expected

    def test_letters(self):
        assert self.view.letters() == ["F", "S"]


class TestGlossaryStateView:
    @pytest.fixture(autouse=True)
    def setup_view(self, portal, request, glossary_content):
        self.g1 = glossary_content["glossary"]
        self.t1 = glossary_content["term1"]
        self.t2 = glossary_content["term2"]
        self.d1 = glossary_content["document"]
        self.view = api.content.get_view(name="glossary_state", context=portal)

    def test_tooltip_is_enabled(self):
        name = IGlossarySettings.__identifier__ + ".enable_tooltip"
        api.portal.set_registry_record(name, True)
        assert self.view.tooltip_is_enabled

        api.portal.set_registry_record(name, False)
        assert not self.view.tooltip_is_enabled

    def test_content_type_is_enabled(self):
        assert not self.view.content_type_is_enabled

        self.view.context = self.d1
        assert self.view.content_type_is_enabled

        self.view.context = self.g1
        assert not self.view.content_type_is_enabled


class TestJsonView:
    @pytest.fixture(autouse=True)
    def setup_view(self, portal, request, glossary_content):
        self.g1 = glossary_content["glossary"]
        self.t1 = glossary_content["term1"]
        self.t2 = glossary_content["term2"]
        self.d1 = glossary_content["document"]
        self.view = api.content.get_view("glossary", portal)

    def test_get_json_entries(self):
        expected = [
            {"term": "FTD", "description": "<p>First Term Description</p>"},
            {"term": "First Term", "description": "<p>First Term Description</p>"},
            {"term": "MFTD", "description": "<p>First Term Description</p>"},
            {"term": "MSTD", "description": "<p>Second Term Description</p>"},
            {"term": "STD", "description": "<p>Second Term Description</p>"},
            {"term": "Second Term", "description": "<p>Second Term Description</p>"},
        ]
        assert self.view.get_json_entries() == expected

    def test_call(self):
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
        assert json.loads(result) == expected
