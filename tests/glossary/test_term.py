import pytest
from collective.glossary.interfaces import ITerm
from plone import api
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import createObject
from zope.component import queryUtility


class TestTermType:
    @pytest.fixture(autouse=True)
    def setup(self, portal):
        with api.env.adopt_roles(["Manager"]):
            self.g1 = api.content.create(portal, "Glossary", "g1")
        self.t1 = api.content.create(self.g1, "Term", "t1")

    def test_adding(self):
        assert ITerm.providedBy(self.t1)

    def test_adding_outside_glossary(self, portal):
        from plone.api.exc import InvalidParameterError

        with pytest.raises(InvalidParameterError):
            api.content.create(portal, "Term", "test")

    def test_fti(self):
        fti = queryUtility(IDexterityFTI, name="Term")
        assert fti is not None

    def test_schema(self):
        fti = queryUtility(IDexterityFTI, name="Term")
        schema = fti.lookupSchema()
        assert schema == ITerm

    def test_factory(self):
        fti = queryUtility(IDexterityFTI, name="Term")
        factory = fti.factory
        new_object = createObject(factory)
        assert ITerm.providedBy(new_object)
