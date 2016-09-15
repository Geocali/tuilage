# tuilage
Georeference images and make tiles

This program takes as input images, and a csv file containing the geographical coordinates of each image.
It then 
- converts the geographical coordinates
- create georeferenced images
- and create tiles from this set of images, in the same format as openstreetmap.org
- create some stats

I used this program to create a GPS map accessible on the cell phone, with the drawings of a civil work project.
This allowed me to have the Autocad drawings of the APS system of the tram of Rio de Janeiro (VLT Rio Porto Maravilha) on my cell phone, and my GPS location on the plan

You can see an example in :
http://www.geocali.com/calepinage/4_tiles
http://www.geocali.com/calepinage/4_tiles/23/3187889/4742587.png

However, the process of creating the tiles requires a huge amount of CPU power.
In order to accelerate the creation of the tiles, I modified the generate_tiles_multiprocess.py so that we can share the calculations of various machines, using Dispy.

On the cell phone side, I simply compiled MapsForge, giving the correct URL of the tiles.

If you are interested in this project, please contact me !