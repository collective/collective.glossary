# -*- coding: utf-8 -*-
from Products.CMFPlone.interfaces import INonInstallable
from zope.interface import implementer


@implementer(INonInstallable)
class HiddenProfiles(object):  # pragma: no cover

    @staticmethod
    def getNonInstallableProfiles():
        """Do not show on Plone's list of installable profiles."""
        return [
            u'collective.glossary:uninstall',
        ]
