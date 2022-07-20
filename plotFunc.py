import matplotlib.pyplot as plt
import math

def plotPoints(points):
	x=[point.x for point in points]
	y=[point.y for point in points]
	plt.plot(x, y, 'o', color='black')

def plotRoads(roads):
	for road in roads:
		plt.plot([road.pointA.x, road.pointB.x], [road.pointA.y, road.pointB.y], c='black')

def carPos(cars, roadWidth):

	# X=[car.road.pointA.x - car.direction.value*roadWidth/4*math.sin(car.road.theta) + (car.road.pointB.x-car.road.pointA.x)*car.position for car in cars]
	# Y=[car.road.pointA.y + car.direction.value*roadWidth/4*math.cos(car.road.theta) + (car.road.pointB.y-car.road.pointA.y)*car.position for car in cars]

	X=[car.road.pointA.x + (car.road.pointB.x-car.road.pointA.x)*car.position for car in cars]
	Y=[car.road.pointA.y + (car.road.pointB.y-car.road.pointA.y)*car.position for car in cars]

	return X,Y
