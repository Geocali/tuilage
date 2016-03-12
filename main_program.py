# -*- coding: UTF-8 -*-
import os
import csv
import imp

# ============ impression des images à partir d'Autocad ================================
#foo=imp.load_source('pilot_acad4','c:/georef/test8/pilot_acad4.py')
#chemin_acad='"C:\\Program Files\\Autodesk\\AutoCAD 2013\\acad.exe"'
#chemin_dvb='C:\\georef\\test8\\DGtoPNG.dvb'
#chemin_dwg='C:\\georef\\test8\\plan_install.dwg'
#nb_tot_process=4
#foo.impression(chemin_acad,chemin_dvb,chemin_dwg,nb_tot_process)


# ============= Géoréférencement des images =============================================

# alternative a l'import : sys.path.append()
foo=imp.load_source('georef','c:/georef/test8/georef.py') # !!!!!!!!!!!!!!!!!!!!!
dossier_in=chemin_dwg[:-4]
dossier_out=chemin_dwg[:-4]
srs1='"+proj=utm +zone=23 +south +ellps=aust_SA +towgs84=-166.65,100.10,52.88,0,0 +no_defs"'
#srs2='"+proj=latlong +ellps=WGS84 +datum=WGS84 +no_defs"'
srs2='"+proj=merc +a=6378137 +b=6378137 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 +y_0=0 +k=1.0 +units=m +nadgrids=@null +no_defs +over"'
foo.georef(dossier_in, dossier_out, srs1, srs2)


# ============= Création des tuiles =========================================
# ---- on commence par créer le fichier xml qui définit la carte ----
foo=imp.load_source('xml_carte', 'c:/georef/test8/xml_carte.py')
dossier_in=dossier_out
mapfile=dossier_in.replace('\\','/') + '/calepinage.xml'
foo.xmlage(dossier_in, srs2, mapfile)

# ---- puis on crée les tuiles ----
foo=imp.load_source('__main__', 'generate_tiles_multiprocess.py') #!!!!!!!!!!!!!!!!!!!!!
tile_dir=dossier_in.replace('\\','/') + '/tiles/'
minZoom=19
maxZoom=23
foo.tuilage(mapfile, tile_dir, minZoom, maxZoom)


# ============= Création d'un fichier avec les temps de création ===============
foo=imp.load_source('stats', 'stats.py') # !!!!!!!!!!!!!!!!!!
foo.stats(dossier_out)