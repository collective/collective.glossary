# -*- coding: utf-8 -*-
from collective.glossary.interfaces import IGlossarySettings
from plone import api
from plone.i18n.normalizer.base import baseNormalize
from Products.Five.browser import BrowserView

import json


class TermView(BrowserView):
    """Default view for Term type"""

    def get_entry(self):
        """Return term information."""
        scales = self.context.unrestrictedTraverse('@@images')
        image = scales.scale('image', None)
        item = {
            'title': self.context.title,
            'description': self.context.description,
            'image': image,
        }
        return item


class GlossaryView(BrowserView):
    """Default view of Glossary type"""

    def get_entries(self):
        """Return information of terms in the glossary."""
        entries = self.context.get_entries()
        items = {}
        for obj in entries:
            index = baseNormalize(obj.title)[0].upper()
            if index not in items:
                items[index] = []
            scales = obj.unrestrictedTraverse('@@images')
            image = scales.scale('image', scale='tile')  # 64x64
            item = {
                'title': obj.title,
                'description': obj.description,
                'image': image,
            }
            items[index].append(item)

        for k in items:
            items[k] = sorted(items[k], key=lambda term: term['title'])

        return items

    def letters(self):
        """Return an index of initial letters of all terms."""
        return sorted(self.get_entries())

    def terms(self, letter):
        """Return all terms starting with a letter."""
        return self.get_entries()[letter]


class GlossaryStateView(BrowserView):
    """Glossary State view used to enable or disable resources

    This is called by JS and CSS resources registry.
    """

    @property
    def tooltip_is_enabled(self):
        """Check if term tooltip is enabled."""
        return api.portal.get_registry_record(
            IGlossarySettings.__identifier__ + '.enable_tooltip')

    @property
    def content_type_is_enabled(self):
        """Check if we must show the tooltip in this context."""
        portal_type = getattr(self.context, 'portal_type', None)
        enabled_content_types = api.portal.get_registry_record(
            IGlossarySettings.__identifier__ + '.enabled_content_types')
        return portal_type in enabled_content_types

    @property
    def is_view_action(self):
        """Check if we are into the view action."""
        context_url = self.context.absolute_url()
        # Check if use Virtual Host configuration (ex.: Nginx)
        request_url = self.request.get('VIRTUAL_URL', None)

        if request_url is None:
            request_url = self.request.base + self.request.get('PATH_INFO', '')

        if context_url == request_url:
            return True

        # Default view
        return context_url.startswith(request_url) and \
            len(context_url) > len(request_url)

    def __call__(self):
        return self.tooltip_is_enabled and \
            self.content_type_is_enabled and self.is_view_action


class JsonView(BrowserView):
    """View that returns all glossary items in JSON format. It is used
    to create the tooltips.
    """

    def is_safe_method(self):
        """Check if the request was made using a safe method."""
        safe_methods = ('GET', 'HEAD')
        return self.request.get('REQUEST_METHOD', 'GET').upper() in safe_methods

    @staticmethod
    def get_entries():
        """Return information of all terms."""
        catalog = api.portal.get_tool('portal_catalog')
        items = []
        for brain in catalog(portal_type='Term'):
            items.append({
                'term': brain.Title,
                'description': brain.Description,
            })

        return items

    def __call__(self):
        """Return information of all terms in JSON format.

        Make use of HTTP caching headers to decrease server usage:
        results are not cached on browsers and are cached 120 seconds
        on intermediate caches.

        More information: https://httpwg.org/specs/rfc7234.html
        """
        response = self.request.response
        if not self.is_safe_method():
            response.setStatus(412)  # Precondition Failed
            return ''

        response.setHeader('Cache-Control', 'max-age=0, s-maxage=120')
        response.setHeader('Content-Type', 'application/json')
        return response.setBody(json.dumps(self.get_entries()))
