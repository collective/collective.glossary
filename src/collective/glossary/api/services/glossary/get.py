# -*- coding: utf-8 -*-

from collections import defaultdict
from collective.glossary.interfaces import IGlossarySettings
from plone import api
from plone.i18n.normalizer.base import baseNormalize
from plone.restapi.services import Service


class GetGlossaryTerms(Service):
    """@glossary_terms"""

    def _error(self, status, type, message):
        self.request.response.setStatus(status)
        return {"error": {"type": type, "message": message}}

    def reply(self):
        """Return dictionary of terms grouped by first letter.

        - transliterated index letter
        - sorted within letter group
        """

        brains = api.content.find(context=self.context, portal_type="Term")
        portal_url = api.portal.get().absolute_url()
        terms = [
            {
                "id": brain["id"],
                "title": brain["Title"],
                "terms": list(brain["variants"]),
                "definition": brain["definition"] or "",
                "@id": brain.getURL().replace(portal_url, ""),
                "description": brain.Description or "",
            }
            for brain in brains
        ]
        # Group by first letter
        items = defaultdict(list)
        for t in terms:
            items[baseNormalize(t["title"])[0].upper()].append(t)
        # sort within letter
        for letter in items:
            items[letter] = sorted(
                items[letter],
                key=lambda el: baseNormalize(el["title"]).upper(),
            )

        settings = {
            "enabled": api.portal.get_registry_record(
                name="enable_tooltip",
                interface=IGlossarySettings,
                default=False,
            ),
            "enabled_types": api.portal.get_registry_record(
                name="enabled_content_types",
                interface=IGlossarySettings,
                default=[],
            ),
        }

        return {
            "items": items,
            "items_total": len(terms),
            "settings": settings,
        }


class GetTooltipTerms(Service):
    """Service @tooltip_terms"""

    def _error(self, status, type, message):
        self.request.response.setStatus(status)
        return {"error": {"type": type, "message": message}}

    def reply(self):
        """Return list of terms.

        Terms are all titles and variants with their list of definitions."""

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
            items.append(
                {
                    "term": title,
                    "definition": terms_with_variants[title],
                }
            )
        items = sorted(
            items,
            key=lambda vrt: vrt["term"].lower(),
        )

        return {
            "items": items,
            "items_total": len(items),
        }
