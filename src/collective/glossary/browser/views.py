from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class TermView(BrowserView):
    """ This does nothing so far
    """
    term = ViewPageTemplateFile("templates/term.pt")

    def __init__(self,
                 context,
                 request):
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

    def __call__(self):
        return self.term()


class GlossaryView(BrowserView):
    """ This does nothing so far
    """

    glossary = ViewPageTemplateFile("templates/glossary.pt")

    def __init__(self,
                 context,
                 request):
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

    def __call__(self):
        return self.glossary()
