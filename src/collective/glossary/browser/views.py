# -*- coding: utf-8 -*-

from collective.glossary.interfaces import IGlossarySettings
from plone import api
from plone.i18n.normalizer.base import baseNormalize
from plone.memoize import ram
from Products.CMFPlone.utils import safe_unicode
from Products.Five.browser import BrowserView

import icu
import json


def _user_cachekey(method, self):
    """Return a cachekey for user."""

    current = api.user.get_current()
    return current and current.id or "anonymous"


class TermView(BrowserView):
    """Default view for Term type"""


class GlossaryView(BrowserView):

    """Default view of Glossary type"""

    @ram.cache(_user_cachekey)
    def get_entries(self):
        """Get glossary entries and keep them in the desired format"""

        catalog = api.portal.get_tool("portal_catalog")
        path = "/".join(self.context.getPhysicalPath())
        query = dict(portal_type="Term", path={"query": path, "depth": 1})

        items = {}
        for brain in catalog(**query):
            obj = brain.getObject()
            index = baseNormalize(obj.title)[0].upper()
            if index not in items:
                items[index] = []
            scales = obj.unrestrictedTraverse("@@images")
            image = scales.scale("image", scale="tile")  # 64x64
            item = {
                "title": obj.title,
                "definition": obj.definition.output,
                "variations": obj.variations,
                "image": image,
                "state": brain.review_state,
            }
            items[index].append(item)

        language = api.portal.get_current_language()
        collator = icu.Collator.createInstance(icu.Locale(str(language)))

        for k in items:
            items[k] = sorted(
                items[k],
                key=lambda term: collator.getSortKey(safe_unicode(term["title"])),
            )

        return items

    def letters(self):
        """Return all letters sorted"""

        return sorted(self.get_entries())

    def terms(self, letter):
        """Return all terms of one letter"""

        return self.get_entries()[letter]


class GlossaryStateView(BrowserView):
    """Glossary State view used to enable or disable resources

    This is called by JS and CSS resources registry
    """

    @property
    def tooltip_is_enabled(self):
        """Check if term tooltip is enabled."""
        return api.portal.get_registry_record(
            IGlossarySettings.__identifier__ + ".enable_tooltip"
        )

    @property
    def content_type_is_enabled(self):
        """Check if we must show the tooltip in this context."""
        portal_type = getattr(self.context, "portal_type", None)
        enabled_content_types = api.portal.get_registry_record(
            IGlossarySettings.__identifier__ + ".enabled_content_types"
        )
        return portal_type in enabled_content_types

    @property
    def is_view_action(self):
        """Check if we are into the view action."""
        context_url = self.context.absolute_url()
        # Check if use Virtual Host configuration (ex.: Nginx)
        request_url = self.request.get("VIRTUAL_URL", None)

        if request_url is None:
            request_url = self.request.base + self.request.get("PATH_INFO", "")

        if context_url == request_url:
            return True

        # Default view
        return context_url.startswith(request_url) and len(context_url) > len(
            request_url
        )

    def __call__(self):
        return (
            self.tooltip_is_enabled
            and self.content_type_is_enabled
            and self.is_view_action
        )


class JsonView(BrowserView):
    """Json view that return all glossary items in json format

    This view is used into an ajax call for
    """

    @ram.cache(_user_cachekey)
    def get_json_entries(self):
        """Get all itens and prepare in the desired format.
        Note: do not name it get_entries, otherwise caching is broken."""

        catalog = api.portal.get_tool("portal_catalog")

        items = []
        for brain in catalog(portal_type="Term"):
            items.append(
                {
                    "term": brain.Title,
                    "definition": brain.getObject().definition.output,
                }
            )

        return items

    def __call__(self):
        response = self.request.response
        response.setHeader("content-type", "application/json")

        return response.setBody(json.dumps(self.get_json_entries()))
