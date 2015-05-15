# -*- coding: utf-8 -*-
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

        return items

    def letters(self):
        return set(self.items.keys())

    def terms(self, letter):
        return self.items[letter]


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
