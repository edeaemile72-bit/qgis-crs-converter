# -*- coding: utf-8 -*-
"""
CRS Converter - Classe principale du plugin.
Enregistre l'action dans le menu Vecteur et la barre d'outils de QGIS.
"""

import os
from qgis.PyQt.QtWidgets import QAction
from qgis.PyQt.QtGui import QIcon


class CrsConverterPlugin:

    def __init__(self, iface):
        self.iface = iface
        self.plugin_dir = os.path.dirname(__file__)
        self.action = None
        self.dialog = None

    def initGui(self):
        icon_path = os.path.join(self.plugin_dir, "icon.png")
        self.action = QAction(
            QIcon(icon_path),
            "Convertisseur de coordonnées (CRS)",
            self.iface.mainWindow()
        )
        self.action.triggered.connect(self.run)

        # Ajout dans le menu Vecteur et dans une barre d'outils
        self.iface.addPluginToVectorMenu("&CRS Converter", self.action)
        self.iface.addToolBarIcon(self.action)

    def unload(self):
        self.iface.removePluginVectorMenu("&CRS Converter", self.action)
        self.iface.removeToolBarIcon(self.action)

    def run(self):
        # Import différé : évite de charger PyQt/openpyxl tant que
        # le plugin n'est pas réellement utilisé
        from .crs_converter_dialog import CrsConverterDialog

        if self.dialog is None:
            self.dialog = CrsConverterDialog(self.iface.mainWindow())
        self.dialog.show()
        self.dialog.raise_()
        self.dialog.activateWindow()
