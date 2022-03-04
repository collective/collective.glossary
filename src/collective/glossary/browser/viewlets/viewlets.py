# -*- coding: utf-8 -*-
from plone.app.layout.viewlets import common as base

import plone.api


class CssJS(base.ViewletBase):
    def portal_url(self):
        return plone.api.portal.get().absolute_url()
