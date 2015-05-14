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
        scales = self.context.restrictedTraverse('@@images')
        image = scales.scale('image', None)
        item = {
            'title': self.context.Title(),
            'description': self.context.Description(),
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
        items = {}

        for brain in self.context.getFolderContents():
            index = brain.Title[0].upper()
            if index not in items:
                items[index] = []
            obj = brain.getObject()
            scales = obj.restrictedTraverse('@@images')
            image = scales.scale('image', None)
            item = {
                'title': brain.Title,
                'description': brain.Description,
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
                'description': brain.Description
            })

        return items

    def __call__(self):
        response = self.request.response
        response.setHeader('content-type', 'application/json')
        return response.setBody(json.dumps(self.items))
