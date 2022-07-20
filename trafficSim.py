import roadsGraph, vehicle, trafficLogic, plotFunc, gui, roadBuilder
import matplotlib.pyplot as plt
from matplotlib import animation
import random
import pathlib

#preload map
mapFile=str(pathlib.Path(__file__).parent.resolve()) + '\\StopLoop.p'

dt=.1
roadWidth=20
stopLine=1.2*roadWidth/2
bumper=5

output = 'screen'
#screen		show animation on screen
#mp4 		save animation to mp4
#gif		save animation to gif

while 1==1:

	
	points, roads, carCount, mapFile = gui.main(mapFile)
	for point in points:
		#flip y coordinate for plotting
		point.y = -point.y

	roadsGraph.addAdjustments(roads, roadWidth)

	cars=[]
	for i in range(carCount):
		#initialise the position, direction (random) and speed (half speed limit) of the car
		roadNum = random.randint(0,len(roads)-1)
		roadPos = random.random()*.6+.2
		roadDir = random.randint(0,1)
		if roadDir == 0:
			roadDir = vehicle.direction.AtoB
		else:
			roadDir = vehicle.direction.BtoA
		initSpeed = random.uniform(0, roads[roadNum].speedLimit/2)
		car = vehicle.vehicle(roads[roadNum],roadPos,roadDir,initSpeed,25,50)

		#decide what road the car will move to next
		trafficLogic.chooseNextRoad(car,roads)
		cars.append(car)

	def init():
		#initialise amination
		carsScatter.set_data([], [])
		return carsScatter,

	def animate(i,cars):

		#move cars one time step
		cars=trafficLogic.step(cars,dt,stopLine,bumper,roads, roadWidth)
		
		#get new car positions and plot
		x,y=plotFunc.carPos(cars, roadWidth)
		carsScatter.set_data(x, y)
		return carsScatter,

	
	xmin, xmax = min([point.x for point in points]), max([point.x for point in points])
	ymin, ymax = min([point.y for point in points]), max([point.y for point in points])
	buff = .1*(xmax-xmin)

	fig,ax = roadBuilder.buildRoads(points, roads, roadWidth)
	carsScatter, = ax.plot([], [], 'o', color='red')

	anim = animation.FuncAnimation(fig, animate, fargs=(cars,), init_func=init, frames=200, interval=1000*dt, blit=True)

	if output == 'screen':
		plt.show()
	elif output == 'mp4':
		anim.save('traffic.mp4', fps=1/dt, extra_args=['-vcodec', 'libx264'])
	elif output == 'gif':
		anim.save('traffic.gif', writer='imagemagick', fps=1/dt)
	