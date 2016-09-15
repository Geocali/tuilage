# -*- coding: UTF-8 -*-

import os
import csv

def georef(dossier_in, dossier_out, srs1, srs2):
	# ========= on convertit les points
	
	file_input=dossier_in + '/pts_carres.csv'
	file_output=dossier_out + '/pts_georef.csv'
	
	command='gdaltransform "-s_srs" ' + srs1 + ' -t_srs ' + srs2 + ' < ' + file_input + ' > ' + file_output
	os.system(command)
	
	csvfile=open(file_output, 'r')
	reader=csv.reader(csvfile, delimiter=" ")
	pts_ref=[]
	for row in reader:
		pts_ref.append(row)
		
	# ========= on géoréférencie l'image
	# --- liste des images à traiter
	
	listing = os.listdir(dossier_in)
	listing.sort()
	images=[]
	for infile in listing:
		nom_image= infile
		len_image=len(nom_image)
		if nom_image[-3:]=='png':
			nom=nom_image[:-4]
			decomp=nom.split('-')
			nb=len(decomp)
			images.append([dossier_in + '/' + nom_image, int(decomp[nb-2]), int(decomp[nb-1])])
	# --- liste des points de géoréférencement
	srs1='"+proj=latlong +ellps=WGS84 +datum=WGS84 +no_defs"'
	ullon2=[]
	ullat2=[]
	lrlon2=[]
	lrlat2=[]
	k=0
	n=0
	for im in images:

		ullon=pts_ref[k][0]
		ullat=pts_ref[k][1]
		lrlon=pts_ref[k+1][0]
		lrlat=pts_ref[k+1][1]
		
		file1=im[0]
		file2=file1.replace('2_printed_images', '3_georef_images')
		file2=file2.replace('png', 'tif')
		n=n+1
		print('georeferencement image ' + str(n) + '/' + str(len(images)) + ' : ' + im[0])
		
		commande="gdal_translate -of GTiff -a_ullr " + " " + ullon + " " + ullat + " " + lrlon + " " + lrlat + " -a_srs " + srs1 + "  -co COMPRESS=JPEG -co JPEG_QUALITY=100 " + file1 + " " +  file2
		os.system(commande)
		
		# On supprime les images géoréférencées qui sont vides
		statinfo = os.stat(file2)
		taille=statinfo.st_size
		if taille==8996904: # l'image ne contient que des pixels blancs
			os.remove(file2)
			print('image ' + file2 + ' deleted')
		else:
			ullon2.append(ullon)
			ullat2.append(ullat)
			lrlon2.append(lrlon)
			lrlat2.append(lrlat)
		
		k=k+2
	# ============= On supprime les png ====================
	listing = os.listdir(dossier_out)
	for infile in listing:
		nom_iop= dossier_out + '/' + infile
		if infile[-3:]=='png':
			print('image png a supprimer')
			#os.remove(nom_iop) !!!!!!!!!!!!!!!!!!!

	# ============== on crée un nouveau fichier excel avec les coordonnées des images non vides ========
	file_output=dossier_out	 + '/pts_georef_finaux.csv'
	file = open(file_output,'w')   # Trying to create a new file or open one
	for i in range(0,len(ullon2)):
		file.write(str(ullon2[i]) + ' ' + str(ullat2[i]) + '\n')
		file.write(str(lrlon2[i]) + ' ' + str(lrlat2[i]) + '\n')
		i=i+1
	file.close()
	
