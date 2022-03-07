# -*- coding: utf-8 -*-
from collective.glossary.interfaces import ITerm
from plone.indexer import indexer


@indexer(ITerm)
def variantsIndexer(context):
    variants = context.variants or []
    return list(variants)


@indexer(ITerm)
def definitionIndexer(context):
    return context.definition.raw
