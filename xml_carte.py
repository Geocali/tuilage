# -*- coding: UTF-8 -*-

import os
import csv
import decimal

def xmlage(dossier_in, srs2, file_output, fichier_pts):
	#srs2='"+proj=merc +a=6378137 +b=6378137 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 +y_0=0 +k=1.0 +units=m +nadgrids=@null +no_defs +over"'
	
	csvfile=open(fichier_pts, 'r')
	reader=csv.reader(csvfile, delimiter=" ")
	pts_ref=[]
	for row in reader:
		pts_ref.append(row)

	#file_output=dossier_in.replace('\\','/') + '/calepinage.xml'
	file = open(file_output,'w')   # Trying to create a new file or open one
	file.write('<?xml version="1.0" encoding="utf-8"?>\n')
	file.write('<Map srs=' + srs2 + ' background-color="rgb(128,128,160)">\n')
	
	listing = os.listdir(dossier_in)
	i=0
	for infile in listing:
		
		if infile[-3:]=='tif':
			file.write('    <Style name="' + infile + '">\n') # !!! dossier_in.replace('..', 'home/cvial/data') + '/' + 
			file.write('        <Rule>\n')
			file.write('            <RasterSymbolizer/>\n')
			file.write('        </Rule>\n')
			file.write('    </Style>\n')
			file.write('    <Layer name="Tif layer" srs=' + srs2 + '>\n')
			file.write('        <StyleName>' + infile + '</StyleName>\n')
			file.write('        <Datasource>\n')
			file.write('            <Parameter name="file">' + infile + '</Parameter>\n')
			nb=float(pts_ref[i+1][0])
			n=nb/1000000
			hix=str(n) + 'e+006'
			file.write('            <Parameter name="hix">' + hix + '</Parameter>\n')
			nb=float(pts_ref[i][1])
			n=nb/1000000
			hiy=str(n) + 'e+006'
			file.write('            <Parameter name="hiy">' + hiy + '</Parameter>\n')
			nb=float(pts_ref[i][0])
			n=nb/1000000
			lox=str(n) + 'e+006'
			file.write('            <Parameter name="lox">' + lox + '</Parameter>\n')
			nb=float(pts_ref[i+1][1])
			n=nb/1000000
			loy=str(n) + 'e+006'
			file.write('            <Parameter name="loy">' + loy + '</Parameter>\n')
			file.write('            <Parameter name="type">raster</Parameter>\n')
			file.write('        </Datasource>\n')
			file.write('    </Layer>\n')
			
			i=i+2

	file.write('</Map>\n')
	file.close()

