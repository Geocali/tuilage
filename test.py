import os
#os.chdir('/home/cvial')
#os.system('ls')
import csv

# os.chdir('/home/cvial/data/drawings/LB00_2016-03-16/2_printed_images/')
# os.system('ls')
# print('iop')

# csvfile=open('/home/cvial/data/drawings/LB00_2016-03-16/2_printed_images/pts_carres.csv', 'r')
# reader=csv.reader(csvfile, delimiter=" ")
# pts_ref=[]
# for row in reader:
	# pts_ref.append(row)
	# print('a')
# print(pts_ref)

listing = os.listdir('/home/cvial/data/drawings/LB00_2016-03-16/3_georef_images/')
print(listing)
listing.sort()
print(listing)