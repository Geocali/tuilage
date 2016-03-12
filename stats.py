
import os, time, csv

def stats(chemin_dossier):
	# 1) fichiers png imprimes par Autocad
	autocad=[]
	for dirname, dirnames, filenames in os.walk(chemin_dossier):
		# print path to all subdirectories first.
		for subdirname in dirnames:
			chemin=os.path.join(dirname, subdirname)
			#print(time.ctime(os.path.getmtime(chemin)))
		# print path to all filenames.
		for filename in filenames:
			chemin=os.path.join(dirname, filename)
			if filename[-3:]=='png' and filename[:3]=='img':
				autocad.append(time.ctime(os.path.getmtime(chemin)))
	autocad.sort()
				
	# 2) fichiers tif georeferences
	georeference=[]
	for dirname, dirnames, filenames in os.walk(chemin_dossier):
		# print path to all subdirectories first.
		for subdirname in dirnames:
			chemin=os.path.join(dirname, subdirname)
			#print(time.ctime(os.path.getmtime(chemin)))
		# print path to all filenames.
		for filename in filenames:
			chemin=os.path.join(dirname, filename)
			if filename[-3:]=='tif':
				georeference.append(time.ctime(os.path.getmtime(chemin)))
	georeference.sort()
				
	# 3) tuiles
	tuiles=[]
	for dirname, dirnames, filenames in os.walk(chemin_dossier):
		# print path to all subdirectories first.
		for subdirname in dirnames:
			chemin=os.path.join(dirname, subdirname)
			#print(time.ctime(os.path.getmtime(chemin)))
		# print path to all filenames.
		for filename in filenames:
			chemin=os.path.join(dirname, filename)
			if filename[-3:]=='png' and filename[:3]!='img':
				tuiles.append(time.ctime(os.path.getmtime(chemin)))
	tuiles.sort()

	file = open(chemin_dossier + '\\stats.txt','w')   # Trying to create a new file or open one
	for kp in autocad:
		file.write('autocad;' + kp + '\n')
	for kp in georeference:
		file.write('georeference;' + kp + '\n')
	for kp in tuiles:
		file.write('tuiles;' + kp + '\n')
	file.close