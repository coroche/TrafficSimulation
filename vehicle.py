from enum import Enum

class vehicle:
  def __init__(self, road, position, direction, speed, acceleration, deceleration, stopped=False, ident=None):
    self.road = road
    self.position = position
    self.direction = direction
    self.speed = speed
    self.acceleration = acceleration
    self.deceleration = deceleration
    self.stopped = stopped
    self.ident = ident

class direction(Enum):
    AtoB = 1
    BtoA = -1

def accelerate(car,dt):
	car.speed += car.acceleration*dt

def decelerate(car,dt,markAsStopped=True):
	if car.speed<car.deceleration*dt:
		car.speed=0
		if markAsStopped:
			car.stopped=True
	else:
		car.speed -= car.deceleration*dt

def distanceToGo(car):
	if car.direction==direction.AtoB:
		return	car.road.length*(1-car.position), car.road.pointB, car.road.endBtype
	elif car.direction==direction.BtoA:
		return car.road.length*car.position, car.road.pointA, car.road.endAtype
