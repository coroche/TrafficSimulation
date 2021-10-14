import roadsGraph, vehicle, trafficLogic, plotFunc
import matplotlib.pyplot as plt
from matplotlib import animation
import random


dt=.1
stopLine=1
bumper=.5

points=[]
xs=[-10,10,20,10]
ys=[0,0,0,10]

for i in range(len(xs)):
	points.append(roadsGraph.point(xs[i],ys[i]))

roads=[]
roads.append(roadsGraph.road(points[0],points[1],roadsGraph.signal.green,roadsGraph.signal.green,2))
roads.append(roadsGraph.road(points[1],points[2],roadsGraph.signal.stop,roadsGraph.signal.green,2))
roads.append(roadsGraph.road(points[1],points[3],roadsGraph.signal.stop,roadsGraph.signal.green,2))


cars=[]
cars.append(vehicle.vehicle(roads[2],.9,vehicle.direction.BtoA,0,1,1))
cars.append(vehicle.vehicle(roads[2],.85,vehicle.direction.BtoA,0,1,1))
cars.append(vehicle.vehicle(roads[2],.8,vehicle.direction.BtoA,0,1,1))
cars.append(vehicle.vehicle(roads[2],.75,vehicle.direction.BtoA,0,1,1))
cars.append(vehicle.vehicle(roads[0],0,vehicle.direction.AtoB,0,1,1))

def init():
    carsScatter.set_data([], [])
    return carsScatter,

def animate(i):
	global cars, roads
	cars=trafficLogic.step(cars,dt,stopLine,bumper,roads)
	x,y=plotFunc.carPos(cars)
	carsScatter.set_data(x, y)
	return carsScatter,

fig = plt.figure()
ax = plt.axes(xlim=(-1, 21), ylim=(-1, 11))
ax.set_aspect('equal', adjustable='box')
plt.axis('off')
carsScatter, = ax.plot([], [], 'o', color='red')
plotFunc.plotRoads(roads)

anim = animation.FuncAnimation(fig, animate, init_func=init, frames=200, interval=1000*dt, blit=True)

#plotFunc.plotCars(cars)
#anim.save('traffic.mp4', fps=1/dt, extra_args=['-vcodec', 'libx264'])
anim.save('traffic.gif', writer='imagemagick', fps=1/dt)
#plt.show()