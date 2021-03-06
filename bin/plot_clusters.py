#!/usr/bin/env python
from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt
import sys
from math import log,pi
from find_clusters import mkClusters,dataToArray
from master_variables import ZONE_OF_AVOIDANCE
import find_clusters 
from matplotlib import rc

def r2d(r) : return r / (2*pi) * 360

def plot_clusters(pts,filename,markerscale,background_img=None):
	rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
	rc('text', usetex=True)
	m = Basemap(projection='moll',lon_0=0,resolution='c')
	if background_img: m.warpimage(background_img)
	else: m.drawmapboundary(fill_color='black')
	m.drawparallels(np.arange(-90.,180.,15.),color='white',linewidth=.5)
	m.drawmeridians(np.arange(0.,420.,15.),color='white',linewidth=.5)
	for px,py,sz,name,alpha in pts:
		x,y = m(r2d(px),r2d(py))
		plt.plot(x,y,'*',color='yellow',markersize=markerscale*log(sz,markerscale), alpha=alpha)
		plt.text(x,y,name.replace("_","-").replace("#","No. "),color='red',size=2)
	# Plot the zone of avoidance
	m.drawparallels([ZONE_OF_AVOIDANCE,-ZONE_OF_AVOIDANCE], color='yellow', linewidth=1)
	x,y=m(0,-(ZONE_OF_AVOIDANCE-2))
	plt.text(x,y,r'$b = %i^{\circ}$' % (-(ZONE_OF_AVOIDANCE)),color='yellow',size=7, ha='center', va='bottom')
	x_,y_=m(0,(ZONE_OF_AVOIDANCE-2))                      
	plt.text(x_,y_,r'$b = %i^{\circ}$' % (ZONE_OF_AVOIDANCE),color='yellow',size=7,ha='center', va='top')
	#plt.title("Galaxy Clusters")
	plt.savefig(filename,dpi=300)

if __name__ == "__main__":
	print "Computing cluster points..."
	cls = mkClusters(sys.argv[1])
	if len(sys.argv) == 5: SZ = int(sys.argv[3])
	elif len(sys.argv) == 4: SZ = int(sys.argv[2])
	else : raise "Incorrect command line arguments"
	print "Culling clusters smaller than", SZ, "..."
	bigguys = filter(lambda x : len(x) > SZ, cls)
	pts = map(lambda x : list(dataToArray(x)[0]) + [len(x),x[0][7],1],bigguys)
	print "Making Plot..."
	if len(sys.argv) == 5: 
		plot_clusters(pts,sys.argv[4],float(SZ),sys.argv[2])
		print "Wrote:",sys.argv[4]
	elif len(sys.argv) == 4: 
		plot_clusters(pts,sys.argv[3],float(SZ))
		print "Wrote:",sys.argv[3]
	else : raise "Incorrect number of command line arguments"
