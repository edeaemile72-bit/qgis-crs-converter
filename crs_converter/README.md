# CRS Converter — Plugin QGIS

Plugin de conversion de coordonnées entre systèmes de référence (CRS),
avec support de :
- **Point unique** (saisie manuelle X/Y)
- **Fichier CSV** (import/export)
- **Fichier Excel `.xlsx` multi-feuilles** (import/export), avec détection
  automatique des colonnes X/Y par en-tête et sélection feuille par feuille.

## 1. Installation

### Option A — via l'interface QGIS (recommandé)
1. Ouvrir QGIS.
2. Menu **Extensions > Gérer et installer les extensions**.
3. Onglet **Installer depuis un ZIP**.
4. Sélectionner le fichier `crs_converter.zip` fourni.
5. Cliquer sur **Installer**.
6. Aller dans l'onglet **Installées** et cocher la case **CRS Converter**
   pour l'activer (si ce n'est pas déjà fait).

### Option B — installation manuelle
1. Décompresser `crs_converter.zip`.
2. Copier le dossier `crs_converter` dans :
   ```
   %APPDATA%\QGIS\QGIS3\profiles\default\python\plugins\
   ```
3. Redémarrer QGIS, puis activer le plugin dans
   **Extensions > Gérer et installer les extensions > Installées**.

## 2. Dépendance : openpyxl (pour l'Excel uniquement)

La conversion Excel nécessite le module `openpyxl` dans l'environnement
Python **de QGIS** (pas celui de Windows). Pour l'installer :

1. Ouvrir le menu Démarrer > **OSGeo4W Shell** (installé avec QGIS), ou dans
   QGIS : **Plugins > Console Python**, ou l'invite de commande QGIS.
2. Exécuter :
   ```
   python -m pip install openpyxl
   ```
3. Redémarrer QGIS.

Si `openpyxl` est absent, le plugin fonctionne quand même normalement pour
les onglets **Point unique** et **CSV** — seul l'onglet Excel affichera un
message d'avertissement expliquant comment l'installer.

## 3. Utilisation

Une fois activé, le plugin apparaît :
- dans le menu **Vecteur > CRS Converter > Convertisseur de coordonnées (CRS)**
- et sous forme d'icône dans la barre d'outils.

### Format degrés-minutes-secondes (DMS)
Depuis la version 3.0, si le **CRS cible** choisi est un CRS **géographique**
(coordonnées en degrés, ex. EPSG:4326), le plugin ajoute automatiquement le
résultat au format DMS (ex. `6°22'13.08"N`) en plus des valeurs décimales,
sur les trois onglets. Si le CRS cible est un CRS **projeté** (coordonnées
en mètres, ex. UTM), le format DMS n'a pas de sens et n'est pas proposé —
le plugin l'indique clairement dans son message de résultat.

### Onglet "Point unique"
Saisir X et Y, choisir le CRS source et le CRS cible (recherche par nom ou
code EPSG dans le sélecteur natif QGIS), cliquer sur **Convertir**. Si le
CRS cible est géographique, une seconde ligne affiche le résultat en DMS.

### Onglet "Fichier CSV"
1. Choisir le fichier CSV d'entrée (le séparateur et les colonnes X/Y sont
   détectés automatiquement, modifiables si besoin).
2. Choisir les CRS source/cible.
3. Cliquer sur **Convertir et exporter le CSV** puis choisir l'emplacement
   du fichier de sortie. Le fichier généré conserve toutes les colonnes
   d'origine et ajoute deux colonnes `X_<EPSG_cible>` / `Y_<EPSG_cible>`,
   plus `Lon_DMS` / `Lat_DMS` si le CRS cible est géographique.

### Onglet "Fichier Excel multi-feuilles"
1. Choisir le fichier `.xlsx`.
2. Le tableau liste automatiquement **toutes les feuilles** du classeur,
   avec détection des colonnes X/Y par en-tête (alias reconnus : x, lon,
   longitude, easting / y, lat, latitude, northing). Décocher les feuilles
   à ignorer, corriger les colonnes si besoin.
3. **Depuis la version 3.1**, chaque feuille dispose de son propre
   sélecteur de **CRS source** (colonne "CRS source (feuille)"), utile
   quand plusieurs feuilles proviennent de systèmes différents. Le CRS
   source par défaut choisi dans le groupe du bas est repris pour chaque
   feuille au chargement, puis modifiable individuellement.
4. Choisir le CRS cible (unique, appliqué à toutes les feuilles).
5. Cliquer sur **Convertir et exporter le classeur Excel**. Un nouveau
   fichier `.xlsx` est généré, avec les colonnes converties ajoutées à la
   suite des données existantes, feuille par feuille (plus `Lon_DMS` /
   `Lat_DMS` si le CRS cible est géographique).

### Onglet "Couche vectorielle chargée" (depuis la version 3.2)
Permet de reprojeter directement une couche vectorielle déjà ouverte dans
QGIS (shapefile, GeoPackage, etc.), sans passer par un export CSV/Excel :
1. Sélectionner la couche dans la liste déroulante (bouton **Actualiser la
   liste** si la couche vient d'être ajoutée au projet).
2. Le CRS source est détecté automatiquement à partir de la couche.
3. Choisir le CRS cible.
4. Cliquer sur **Convertir et ajouter au projet** : une nouvelle couche
   mémoire reprojetée est ajoutée au projet QGIS (la couche d'origine
   n'est jamais modifiée). Pour la conserver de façon permanente, faites
   ensuite un clic droit sur la couche > **Exporter > Enregistrer les
   entités sous...**.

### Journal d'erreurs détaillé (depuis la version 3.3)
Sur les onglets **CSV** et **Excel**, une case à cocher "Générer un
journal d'erreurs détaillé (.log)" permet d'obtenir, en plus du message
de synthèse, un fichier texte listant précisément chaque ligne (et,
pour l'Excel, chaque feuille) n'ayant pas pu être convertie, avec les
valeurs en cause et la raison de l'échec. Le fichier est enregistré à
côté du fichier converti, avec le suffixe `_erreurs.log`.

### Bouton Aide (depuis la version 3.4)
Un bouton **Aide** est présent en bas de la fenêtre du plugin, quel que soit
l'onglet actif. Il affiche des instructions contextuelles correspondant à
l'onglet actuellement sélectionné (Point unique, CSV, Excel ou Couche
vectorielle), sans avoir besoin de sortir du plugin ni de consulter ce
README.

## 4. Développement / modifications

Le code est organisé ainsi :
- `crs_converter.py` : enregistrement du plugin dans QGIS (menu, icône).
- `crs_converter_dialog.py` : toute la logique métier et l'interface
  (3 onglets), sans fichier `.ui` — tout est construit en PyQt pur pour
  rester facile à modifier avec Claude Code.

Pour recharger le plugin pendant le développement sans redémarrer QGIS,
installer le plugin **Plugin Reloader**.
