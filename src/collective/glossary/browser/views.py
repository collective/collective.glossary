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
        self.populate()

    def populate(self):
        scales = self.context.restrictedTraverse('@@images')
        image = scales.scale('image', None)
        item = {
            'title': self.context.Title(),
            'description': self.context.Description(),
            'image': image
        }
        self.item = item


class GlossaryView(BrowserView):
    """ This does nothing so far
    """

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.populate()

    def populate(self):
        items = {}

        for brain in self.context.getFolderContents():
            obj = brain.getObject()
            index = brain.Title[0].upper()
            if index not in items:
                items[index] = []
            scales = obj.restrictedTraverse('@@images')
            image = scales.scale('image', None)
            item = {
                'title': obj.Title(),
                'description': obj.Description(),
                'image': image
            }
            items[index].append(item)

        self.items = items

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
        self.data = self.populate()

    @ram.cache(_catalog_counter_cachekey)
    def populate(self):
        catalog = api.portal.get_tool('portal_catalog')

        data = []
        for brain in catalog(portal_type='Term'):
            data.append({
                'term': brain.Title,
                'description': brain.Description
            })

        return data

    def __call__(self):
        response = self.request.response
        response.setHeader('content-type', 'application/json')
        return response.setBody(json.dumps(self.data))
