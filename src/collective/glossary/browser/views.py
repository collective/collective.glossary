# -*- coding: utf-8 -*-

from collective.glossary.interfaces import IGlossarySettings
from plone import api
from plone.i18n.normalizer.base import baseNormalize
from plone.memoize import ram
from Products.CMFPlone.utils import safe_unicode
from Products.Five.browser import BrowserView

import json
import zope.ucol


def _catalog_counter_cachekey(method, self):
    """Return a cachekey based on catalog updates."""

    catalog = api.portal.get_tool('portal_catalog')
    return str(catalog.getCounter())


class TermView(BrowserView):

    """Default view for Term type"""

    # TODO: remove, it's not used anymore
    def get_entry(self):
        """Get term in the desired format"""

        scales = self.context.unrestrictedTraverse('@@images')
        image = scales.scale('image', None)
        item = {
            'title': self.context.title,
            'description': self.context.description,
            'image': image,
        }
        return item

    @property
    def use_rich_text(self):
        """"""

        return api.portal.get_registry_record(
            IGlossarySettings.__identifier__ + '.enable_rich_text_description')


class GlossaryView(BrowserView):

    """Default view of Glossary type"""

    @ram.cache(_catalog_counter_cachekey)
    def get_entries(self):
        """Get glossary entries and keep them in the desired format"""

        catalog = api.portal.get_tool('portal_catalog')
        path = '/'.join(self.context.getPhysicalPath())
        query = dict(portal_type='Term', path={'query': path, 'depth': 1})

        items = {}
        for brain in catalog(**query):
            obj = brain.getObject()
            index = baseNormalize(obj.title)[0].upper()
            if index not in items:
                items[index] = []
            scales = obj.unrestrictedTraverse('@@images')
            image = scales.scale('image', scale='tile')  # 64x64
            text = obj.text.output if getattr(obj, 'text', None) else ''
            item = {
                'title': obj.title,
                'description': obj.description,
                'image': image,
                'text': text,
            }
            items[index].append(item)

        language = api.portal.get_current_language()
        collator = zope.ucol.Collator(str(language))

        for k in items:
            items[k] = sorted(items[k], key=lambda term: collator.key(safe_unicode(term['title'])))

        return items

    def letters(self, filtered=False):
        """Return all letters sorted"""
        entries = self.get_entries()

        if self.enable_letter_filtering and filtered:
            filtering_letter = self.request.form.get('letter', None)
            if filtering_letter in entries:
                return [filtering_letter]

        return sorted(entries)

    def terms(self, letter):
        """Return all terms of one letter"""
        return self.get_entries()[letter]

    @property
    def use_rich_text(self):
        """"""

        return api.portal.get_registry_record(
            IGlossarySettings.__identifier__ + '.enable_rich_text_description')

    @property
    def enable_letter_filtering(self):
        return api.portal.get_registry_record(
            IGlossarySettings.__identifier__ + '.enable_letter_filtering',
            default=False)


class GlossaryStateView(BrowserView):
    """Glossary State view used to enable or disable resources

    This is called by JS and CSS resources registry
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
    """Json view that return all glossary items in json format

    This view is used into an ajax call for
    """

    @ram.cache(_catalog_counter_cachekey)
    def get_json_entries(self):
        """Get all itens and prepare in the desired format.
        Note: do not name it get_entries, otherwise caching is broken. """

        catalog = api.portal.get_tool('portal_catalog')

        items = []
        for brain in catalog(portal_type='Term'):
            items.append({
                'term': brain.Title,
                'description': brain.Description,
            })

        return items

    def __call__(self):
        response = self.request.response
        response.setHeader('content-type', 'application/json')

        return response.setBody(json.dumps(self.get_json_entries()))
