# -*- coding: utf-8 -*-
from collective.glossary import _
from collective.glossary.interfaces import IGlossarySettings
from plone.app.registry.browser import controlpanel


class GlossarySettingsEditForm(controlpanel.RegistryEditForm):

    """Control panel edit form."""

    schema = IGlossarySettings
    label = _(u'Glossary')
    description = _(u'Settings for the collective.glossary package')


class GlossarySettingsControlPanel(controlpanel.ControlPanelFormWrapper):

    """Control panel form wrapper."""

    form = GlossarySettingsEditForm
