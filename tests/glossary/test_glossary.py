import pytest
from collective.glossary.interfaces import IGlossary
from plone import api
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import createObject
from zope.component import queryUtility


class TestGlossaryType:
    @pytest.fixture(autouse=True)
    def setup(self, portal):
        with api.env.adopt_roles(["Manager"]):
            self.g1 = api.content.create(portal, "Glossary", "g1")

    def test_adding(self):
        assert IGlossary.providedBy(self.g1)

    def test_fti(self):
        fti = queryUtility(IDexterityFTI, name="Glossary")
        assert fti is not None

    def test_schema(self):
        fti = queryUtility(IDexterityFTI, name="Glossary")
        schema = fti.lookupSchema()
        assert schema == IGlossary

    def test_factory(self):
        fti = queryUtility(IDexterityFTI, name="Glossary")
        factory = fti.factory
        new_object = createObject(factory)
        assert IGlossary.providedBy(new_object)

    def test_is_selectable_as_folder_default_view(self, portal):
        portal.setDefaultPage("g1")
        assert portal.default_page == "g1"

    def test_not_allowed_content_types(self):
        from plone.api.exc import InvalidParameterError

        with pytest.raises(InvalidParameterError):
            api.content.create(self.g1, "Document", "test")
