# -*- coding: utf-8 -*-
from plone.app.registry.browser import controlpanel
from collective.glossary import _
from collective.glossary.interfaces import IGlossarySettings


class GlossarySettingsEditForm(controlpanel.RegistryEditForm):

    """Control panel edit form."""

    schema = IGlossarySettings
    label = _(u'Finger Pointing')
    description = _(u'Settings for the collective.glossary package')


class GlossarySettingsControlPanel(controlpanel.ControlPanelFormWrapper):

    """Control panel form wrapper."""

    form = GlossarySettingsEditForm
