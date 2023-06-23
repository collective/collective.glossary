# -*- coding: utf-8 -*-

from collections import defaultdict
from collective.glossary.interfaces import IGlossarySettings
from plone import api
from plone.i18n.normalizer.base import baseNormalize
from Products.Five.browser import BrowserView

import json


class TermView(BrowserView):
    """Default view for Term type"""


class GlossaryView(BrowserView):
    """Default view of Glossary type"""

    def _get_entries(self):
        """Get glossary entries and keep them in the desired format"""
        catalog = api.portal.get_tool("portal_catalog")
        path = "/".join(self.context.getPhysicalPath())
        query = dict(portal_type="Term", path={"query": path, "depth": 1})

        items = defaultdict(list)
        for brain in catalog(**query):
            obj = brain.getObject()
            index = baseNormalize(obj.title)[0].upper()
            scales = obj.unrestrictedTraverse("@@images")
            image = scales.scale("image", scale="tile")  # 64x64
            item = {
                "title": obj.title,
                "definition": obj.definition and obj.definition.output or "",
                "variants": obj.variants,
                "image": image,
                "state": brain.review_state,
                "url": obj.absolute_url(),
            }
            items[index].append(item)

        for k in items:
            items[k] = sorted(
                items[k],
                key=lambda term: term["title"],
            )
        return items

    def get_entries(self):
        entries = getattr(self, "_entries", None)
        if entries is None:
            entries = self._get_entries()
            self._entries = entries
        return entries

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

    This view is used for Plone Classic UI
    """

    def get_json_entries(self):
        """Get all terms.

        Return list of term / description dictionaries ready for tooltips:
        description is a collection of all found variants

        Note: do not name it get_entries, otherwise caching is broken."""

        catalog = api.portal.get_tool("portal_catalog")

        terms = catalog(portal_type="Term")
        terms_with_variants = defaultdict(list)
        for term in terms:
            obj = term.getObject()
            terms_with_variants[term.Title].append(
                obj.definition and obj.definition.output or ""
            )
            for vrt in obj.variants:
                terms_with_variants[vrt].append(
                    obj.definition and obj.definition.output or ""
                )

        items = []
        for title in terms_with_variants:
            if len(terms_with_variants[title]) > 1:
                description = f"<ol>{''.join([f'<li>{el}</li>' for el in terms_with_variants[title]])}</ol>"
            elif len(terms_with_variants[title]) == 1:
                description = terms_with_variants[title][0]
            else:
                description = ""

            items.append(
                {
                    "term": title,
                    "description": description,
                }
            )

        items = sorted(
            items,
            key=lambda vrt: vrt["term"],
        )

        return items

    def __call__(self):
        response = self.request.response
        response.setHeader("content-type", "application/json")
        return response.setBody(json.dumps(self.get_json_entries()))
