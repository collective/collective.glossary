# -*- coding: utf-8 -*-

from collective.glossary.interfaces import IGlossarySettings
from plone import api
from plone.restapi.services import Service


SERVICE_NAME = "@glossary_terms"


class GetGlossaryTerms(Service):
    def _error(self, status, type, message):
        self.request.response.setStatus(status)
        return {"error": {"type": type, "message": message}}

    def reply(self):
        brains = api.content.find(context=self.context, portal_type="Term")

        terms = [
            {
                "id": brain["id"],
                "title": brain["Title"],
                "terms": list(brain["variants"]),
                "definition": brain["definition"] or "",
                "url": brain.getURL(),
                "description": brain.Description or "",
            }
            for brain in brains
        ]
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
            "terms": terms,
            "settings": settings,
        }
