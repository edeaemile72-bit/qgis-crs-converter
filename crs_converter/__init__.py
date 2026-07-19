# -*- coding: utf-8 -*-
"""
CRS Converter - Plugin QGIS
Point d'entrée du plugin. QGIS appelle classFactory() au chargement.
"""


def classFactory(iface):
    from .crs_converter import CrsConverterPlugin
    return CrsConverterPlugin(iface)
