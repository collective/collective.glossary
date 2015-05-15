# -*- coding: utf-8 -*-
from collective.glossary.interfaces import IGlossary
from collective.glossary.interfaces import ITerm
from plone import api
from plone.memoize import ram
from Products.Five.browser import BrowserView

import json


def _catalog_counter_cachekey(method, self):
    """Return a cachekey based on catalog updates."""
    catalog = api.portal.get_tool('portal_catalog')
    return str(catalog.getCounter())


class TermView(BrowserView):
    """ This does nothing so far
    """

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.item = self.prepare_item()

    def prepare_item(self):
        scales = self.context.unrestrictedTraverse('@@images')
        image = scales.scale('image', None)
        item = {
            'title': self.context.title,
            'description': self.context.description,
            'image': image
        }
        return item


class GlossaryView(BrowserView):
    """ This does nothing so far
    """

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.items = self.prepare_items()

    def prepare_items(self):
        catalog = api.portal.get_tool('portal_catalog')
        path = '/'.join(self.context.getPhysicalPath())
        query = dict(portal_type='Term', path={'query': path, 'depth': 1})

        items = {}
        for brain in catalog(**query):
            obj = brain.getObject()
            index = obj.title[0].upper()
            if index not in items:
                items[index] = []
            scales = obj.unrestrictedTraverse('@@images')
            image = scales.scale('image', None)
            item = {
                'title': obj.title,
                'description': obj.description,
                'image': image
            }
            items[index].append(item)

        keys = items.keys()
        for k in keys:
            items[k] = sorted(
                items[k],
                key=lambda term: term['title']
            )

        return items

    def letters(self):
        return sorted(self.items.keys())

    def terms(self, letter):
        return self.items[letter]


class GlossaryStateView(BrowserView):
    """ This does nothing so far
    """

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def enable_tooltip(self):
        """
        """
        return api.portal.get_registry_record(
            'collective.glossary.interfaces.IGlossarySettings.enable_tooltip'
        )

    def is_edit_mode(self):
        """
        """
        action = self.request.getURL()
        action = action.split('/')[-1]
        return action in ['edit', 'atct_edit']

    def is_glossary_object(self):
        real_context = self.request.PARENTS
        if len(real_context) == 0:
            return False
        real_context = real_context[0]
        return IGlossary.providedBy(real_context) or ITerm.providedBy(real_context)

    def __call__(self):
        return self.enable_tooltip() and not self.is_edit_mode() and not self.is_glossary_object()


class JsonView(BrowserView):
    """ This does nothing so far
    """

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.items = self.prepare_items()

    @ram.cache(_catalog_counter_cachekey)
    def prepare_items(self):
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
        return response.setBody(json.dumps(self.items))
