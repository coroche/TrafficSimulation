import math
from enum import Enum

class point:
  def __init__(self, x, y):
    self.x = x
    self.y = y

class road:
  def __init__(self, pointA, pointB, endAtype, endBtype, speedLimit):
    self.pointA = pointA
    self.pointB = pointB
    self.endAtype = endAtype
    self.endBtype = endBtype
    self.speedLimit = speedLimit
    self.length = math.sqrt((pointB.x-pointA.x)**2+(pointB.y-pointA.y)**2)

class signal(Enum):
    green = 1
    red = 2
    stop = 3

def roadsFromPoint(point,roads):
	roadOptions=[road for road in roads if road.pointA==point or road.pointB==point]
	return roadOptions

