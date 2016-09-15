#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from math import pi,cos,sin,log,exp,atan
import sys, os, time
import dispy

import mapnik

DEG_TO_RAD = pi/180
RAD_TO_DEG = 180/pi


def minmax (a,b,c):
	a = max(a,b)
	a = min(a,c)
	return a

def setup():
	# define global variables for the nodes
	from math import pi,cos,sin,log,exp,atan
	global pi,cos,sin,log,exp,atan
	global DEG_TO_RAD, RAD_TO_DEG
	DEG_TO_RAD = pi/180
	RAD_TO_DEG = 180/pi
	return 0
	
class GoogleProjection:
	def __init__(self,levels=18):
		self.Bc = []
		self.Cc = []
		self.zc = []
		self.Ac = []
		c = 256
		for d in range(0,levels):
			e = c/2;
			self.Bc.append(c/360.0)
			self.Cc.append(c/(2 * pi))
			self.zc.append((e,e))
			self.Ac.append(c)
			c *= 2
				
	def fromLLtoPixel(self,ll,zoom):
		 d = self.zc[zoom]
		 e = round(d[0] + ll[0] * self.Bc[zoom])
		 f = minmax(sin(DEG_TO_RAD * ll[1]),-0.9999,0.9999)
		 g = round(d[1] + 0.5*log((1+f)/(1-f))*-self.Cc[zoom])
		 return (e,g)
	 
	def fromPixelToLL(self,px,zoom):
		 e = self.zc[zoom]
		 f = (px[0] - e[0])/self.Bc[zoom]
		 g = (px[1] - e[1])/-self.Cc[zoom]
		 h = RAD_TO_DEG * ( 2 * atan(exp(g)) - 0.5 * pi)
		 return (f,h)

def render_tile(x, y, z, mapfile, maxZoom, tile_uri, i_tuile, name):
	import mapnik
	
	print('debut job' + str(i_tuile))
	m = mapnik.Map(256, 256)

	# Load style XML
	mapnik.load_map(m, mapfile, True)

	# Obtain <Map> projection
	prj = mapnik.Projection(m.srs)

	# Projects between tile pixel co-ordinates and LatLong (EPSG:4326)
	tileproj = GoogleProjection(maxZoom+1)

	exists= ""
	if os.path.isfile(tile_uri):
		exists= "exists"
	else:
		#render_tile(tile_uri, x, y, z)
		# !!!!!!!!!!! debut insertion render_tile
		# Calculate pixel positions of bottom-left & top-right
		p0 = (x * 256, (y + 1) * 256)
		p1 = ((x + 1) * 256, y * 256)

		# Convert to LatLong (EPSG:4326)
		l0 = tileproj.fromPixelToLL(p0, z);
		l1 = tileproj.fromPixelToLL(p1, z);

		# Convert to map projection (e.g. mercator co-ords EPSG:900913)
		c0 = prj.forward(mapnik.Coord(l0[0],l0[1]))
		c1 = prj.forward(mapnik.Coord(l1[0],l1[1]))

		# Bounding box for the tile
		if hasattr(mapnik,'mapnik_version') and mapnik.mapnik_version() >= 800:
			bbox = mapnik.Box2d(c0.x,c0.y, c1.x,c1.y)
		else:
			bbox = mapnik.Envelope(c0.x,c0.y, c1.x,c1.y)
		render_size = 256
		m.resize(render_size, render_size)
		m.zoom_to_box(bbox)
		if(m.buffer_size < 128):
			m.buffer_size = 128

		# Render image with default Agg renderer !!!!!!!!!!!!!!!!!!!!! la partie a distribuer est ici !
		im = mapnik.Image(render_size, render_size)
		mapnik.render(m, im)
		im.save(tile_uri, 'png256')
		# !!!!!!!!!!! fin insertion render_tile

		bytes=os.stat(tile_uri)[6]
		empty= ''
		if bytes == 103:
			empty = " Empty Tile "
		print name, ":", z, x, y, exists, empty, "(tuile ", i_tuile, ")"
		# !!!!!!!!!!!!!! fin insertion loop

		 
def render_tiles(bbox, mapfile, tile_dir, minZoom=1,maxZoom=18, name="unknown", ip_master='192.168.99.100', ip_nodes=['192.168.99.101', '192.168.99.102', '192.168.99.103']):
	#print "render_tiles(",bbox, mapfile, tile_dir, minZoom,maxZoom, name,")"
	
	cluster = dispy.JobCluster(render_tile, nodes = ip_nodes, ip_addr = ip_master, depends = [GoogleProjection], setup=setup) # !!!!!!!!!!!!!!!!!!
	jobs = []
	
	if not os.path.isdir(tile_dir):
		 os.mkdir(tile_dir)

	gprj = GoogleProjection(maxZoom+1) 

	ll0 = (bbox[0],bbox[3])
	ll1 = (bbox[2],bbox[1])

	i_tuile=0
	for z in range(minZoom,maxZoom + 1):
		px0 = gprj.fromLLtoPixel(ll0,z)
		px1 = gprj.fromLLtoPixel(ll1,z)

		# check if we have directories in place
		zoom = "%s" % z
		if not os.path.isdir(tile_dir + zoom):
			os.mkdir(tile_dir + zoom)
		for x in range(int(px0[0]/256.0),int(px1[0]/256.0)+1):
			# Validate x co-ordinate
			if (x < 0) or (x >= 2**z):
				continue
			# check if we have directories in place
			str_x = "%s" % x
			if not os.path.isdir(tile_dir + zoom + '/' + str_x):
				os.mkdir(tile_dir + zoom + '/' + str_x)
			
			for y in range(int(px0[1]/256.0),int(px1[1]/256.0)+1):
				# Validate x co-ordinate
				if (y < 0) or (y >= 2**z):
					continue
				str_y = "%s" % y
				tile_uri = tile_dir + zoom + '/' + str_x + '/' + str_y + '.png'
				# Submit tile to be rendered into the queue
				t = (name, tile_uri, x, y, z)
				# !!!!!!!!!!!!!! debut insertion loop
				i_tuile=i_tuile+1
				job = cluster.submit(x, y, z, mapfile, maxZoom, tile_uri, i_tuile, name)
				print('job envoyé' + str(i_tuile))
				job.id = i_tuile
				jobs.append(job)
	
	print(str(i_tuile) + ' tuiles à faire !')
	# nb_done = 0
	# print('nb tuiles : ' + str(i_tuile))
	# while nb_done < i_tuile:
		# print('nb_done ' + str(nb_done))
		# time.sleep(5)
		# nb_done_i=0
		# for job in jobs:
			# print('job')
			# if not(job is None):
				# nb_done_i = nb_done_i +1
		# if nb_done_i > nb_done:
			# nb_done = nb_done_i
			# print(str(nb_done) + '/' + str(i_tuile))
	
	# tuiles=0
	# while tuiles < i_tuile:
		# time.sleep(1)
		# tuile_f=0
		# for dirname, dirnames, filenames in os.walk(tile_dir):
			#print path to all subdirectories first.
			# for subdirname in dirnames:
				# chemin=os.path.join(dirname, subdirname)
				#print(time.ctime(os.path.getmtime(chemin)))
			#print path to all filenames.
			# for filename in filenames:
				# chemin=os.path.join(dirname, filename)
				# if filename[-3:]=='png' and filename[:3]!='img':
					# tuile_f=tuile_f+1
		# if tuile_f > tuiles:
			# tuiles = tuile_f
			# print('done : ' + str(tuiles) + '/' + str(i_tuile))
		# print(str())
		
	cluster.wait()
	print('nombre total de tuiles : ' + str(i_tuile))
	cluster.print_status()
	


def tuilage(mapfile, tile_dir, minZoom, maxZoom):

	if __name__ == "__main__":
		
		# on r?cup?re la d?finition de la zone de la carte
		m=mapnik.Map(500, 500)
		xmin=9999999999999999
		xmax=-9999999999999999
		ymin=9999999999999999
		ymax=-9999999999999999
		mapnik.load_map(m, mapfile)
		i=0
		for iop in m.layers:
			lyr=m.layers[i]
			e=lyr.envelope()
			if xmin > e[0]:
				xmin=e[0]
			if xmin > e[2]:
				xmin=e[2]
			if xmax < e[0]:
				xmax=e[0]
			if xmax < e[2]:
				xmax=e[2]
			if ymin > e[1]:
				ymin=e[1]
			if ymin > e[3]:
				ymin=e[3]
			if ymax < e[1]:
				ymax=e[1]
			if ymax < e[3]:
				ymax=e[3]
			i=i+1
		
		#lyr=m.layers[0]
		#e=lyr.envelope() # e a des coordonnees en mercator spherique, alors que le bbox doit avoir des coordonnees en 4326
		try:
			spherical_merc = mapnik.Projection('+init=epsg:900913')
		except: # you don't have 900913 in /usr/share/proj/epsg
			spherical_merc = mapnik.Projection('+proj=merc +a=6378137 +b=6378137 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 +y_0=0 +k=1.0 +units=m +nadgrids=@null +no_defs +over')
		try:
			longlat = mapnik.Projection('+init=epsg:4326')
		except: # your proj4 files are broken
			longlat = mapnik.Projection('+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs')
		to_srs,from_srs = longlat, spherical_merc
		ct = mapnik.ProjTransform(from_srs,to_srs)
		#longlat_coords1 = mapnik.Coord(e[0], e[1])
		longlat_coords1 = mapnik.Coord(xmin, ymin)
		merc_coords1 = ct.forward(longlat_coords1)
		#longlat_coords2 = mapnik.Coord(e[2], e[3])
		longlat_coords2 = mapnik.Coord(xmax, ymax)
		merc_coords2 = ct.forward(longlat_coords2)
		bbox=(merc_coords1.x,merc_coords1.y,merc_coords2.x,merc_coords2.y)
		
		# on cr?e les tuiles
		render_tiles(bbox, mapfile, tile_dir, minZoom, maxZoom, "Calepinage")

	

	

	
	
