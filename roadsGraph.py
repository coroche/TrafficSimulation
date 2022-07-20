import math
from enum import Enum
import random

class point:
  def __init__(self, x, y, cnvObj=None):
    self.x = x
    self.y = y
    self.cnvObj = cnvObj

class road:
	def __init__(self, pointA, pointB, endAtype, endBtype, speedLimit, cnvObj=None, cnvObj_Start=None, cnvObj_End=None):
		self.pointA = pointA
		self.pointB = pointB
		self.endAtype = endAtype
		self.endBtype = endBtype
		self.speedLimit = speedLimit
		self.length = math.sqrt((pointB.x-pointA.x)**2+(pointB.y-pointA.y)**2)
		self.cnvObj = cnvObj
		self.cnvObj_Start = cnvObj_Start
		self.cnvObj_End = cnvObj_End
		self.theta = self.roadAngle()
		self.pointAAdj = []
		self.pointBAdj = []
	
	def roadAngle(self):
		x0, y0 = self.pointA.x, -self.pointA.y
		x1, y1 = self.pointB.x, -self.pointB.y
		op = y1-y0
		adj = x1-x0
		
		if adj!=0:
			alpha = math.atan(abs(op)/abs(adj))
		
		if op == 0:
			if adj>0:
				theta=0
			else:
				theta=math.pi

		elif adj == 0:
				theta=op/abs(op)*math.pi/2
		
		elif op>0 and adj>0:
			theta=alpha
		elif op<0 and adj>0:
			theta=-alpha
		elif op>0 and adj<0:
			theta=math.pi - alpha
		elif op<0 and adj<0:
			theta=math.pi + alpha
		return theta



class signal(Enum):
    green = 0
    red = 1
    stop = 2

signalColours = {
  'green': 'green',
  'red': 'red',
  'stop': 'orange',
}

def roadsFromPoint(point,roads):
	roadOptions=[road for road in roads if road.pointA==point or road.pointB==point]
	return roadOptions

def calcAdjustment(road1,road2, roadWidth):
	point = [point for point in [road1.pointA,road1.pointB] if point in [road2.pointA,road2.pointB]][0]

	if point == road1.pointB:
		theta1 = road1.theta
	elif point == road1.pointA:
		theta1 = math.pi - road1.theta

	if point == road2.pointA:
		theta2 = road2.theta
	elif point == road2.pointB:
		theta2 = math.pi - road2.theta

	alpha = theta1 - theta2 
	if alpha%math.pi==0:
		roadAdj=0
	else:
		roadAdj = roadWidth/(4*math.sin(alpha))
	relRoadAdj = roadAdj/road1.length

	return relRoadAdj
			

def addAdjustments(roads, roadWidth):
	for road in roads:

		#PointA
		options = [option for option in roadsFromPoint(road.pointA,roads) if option!=road]
		for option in options:
			# road.pointAAdj.append(calcAdjustment(road,option,roadWidth))
			road.pointAAdj.append(0)

		#PointB
		options = [option for option in roadsFromPoint(road.pointB,roads) if option!=road]
		for option in options:
			# road.pointBAdj.append(calcAdjustment(road,option,roadWidth))
			road.pointBAdj.append(0)


		

