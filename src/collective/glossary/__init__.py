"""Init and utils."""

from zope.i18nmessageid import MessageFactory

import logging


__version__ = "3.0.0"

PACKAGE_NAME = "collective.glossary"

_ = MessageFactory(PACKAGE_NAME)

logger = logging.getLogger(PACKAGE_NAME)
