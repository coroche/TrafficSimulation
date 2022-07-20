import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib as mpl
import math
import roadsGraph

#test inputs
# points=[]
# xs=[-10,10,20,10]
# ys=[0,0,0,10]

# for i in range(len(xs)):
# 	points.append(roadsGraph.point(xs[i],ys[i]))

# roads=[]
# roads.append(roadsGraph.road(points[0],points[1],roadsGraph.signal.green,roadsGraph.signal.green,2))
# roads.append(roadsGraph.road(points[1],points[2],roadsGraph.signal.stop,roadsGraph.signal.green,2))
# roads.append(roadsGraph.road(points[1],points[3],roadsGraph.signal.stop,roadsGraph.signal.green,2))

#width=10
def buildRoads(points, roads, width):
	

	fig, ax = plt.subplots()	
	for road in roads:
		
		ts = ax.transData
		t = mpl.transforms.Affine2D().translate(0,-width/2)
		r = mpl.transforms.Affine2D().rotate_around(road.pointA.x, road.pointA.y, road.theta)
		
		trans = t + r + ts
		rec = patches.Rectangle((road.pointA.x,road.pointA.y), road.length, width, color='k', transform=trans)
		cir1 = plt.Circle((road.pointA.x,road.pointA.y),width/2,color='black')
		cir2 = plt.Circle((road.pointB.x,road.pointB.y),width/2,color='black')
		
		ax.add_patch(rec)
		ax.add_patch(cir1)
		ax.add_patch(cir2)
		plt.plot([road.pointA.x, road.pointB.x], [road.pointA.y, road.pointB.y], c='y', ls='--')

	xmax, xmin = max([point.x for point in points]), min([point.x for point in points])
	ymax, ymin = max([point.y for point in points]), min([point.y for point in points])


	plt.xlim([xmin-width, xmax+width])
	plt.ylim([ymin-width, ymax+width])
	
	fig.patch.set_facecolor('forestgreen')
	ax.set_aspect('equal', adjustable='box')		#equal aspect to avoid stretching squishing
	plt.axis('off')
	return fig,ax
	#plt.show()

#buildRoads(points,roads, width)
	