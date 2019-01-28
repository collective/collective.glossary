import plone.api

from plone.app.layout.viewlets import common as base


class CssJS(base.ViewletBase):

    def portal_url(self):
        return plone.api.portal.get().absolute_url()
