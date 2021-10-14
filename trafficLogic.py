import roadsGraph, vehicle
import random


def chooseNewRoad(car,intersection,roads):
			roadOptions=[road for road in roadsGraph.roadsFromPoint(intersection,roads) if road!=car.road]
			if len(roadOptions)==0:
				return False
			else:
				car.road=roadOptions[random.randint(0,len(roadOptions)-1)]
				if intersection==car.road.pointA:
					car.position=abs(car.position)%1
					car.direction=vehicle.direction.AtoB
				else:
					car.position=1-abs(car.position)%1
					car.direction=vehicle.direction.BtoA
				car.stopped=False
			return True


def step(cars, dt, stopLine, bumper, roads):
	for car in list(cars):
		
		ds=car.speed*dt
		car.position += car.direction.value*ds/car.road.length
		stoppingDistance=car.speed**2/(2*car.deceleration)
		distanceToEnd, intersection, signal = vehicle.distanceToGo(car)
		
		otherCars=[(otherCar.position-car.position)*car.direction.value for otherCar in cars if otherCar!=car and otherCar.road==car.road and otherCar.direction==car.direction]		
		otherCarsInFront=[otherCar for otherCar in otherCars if otherCar>0]
		if otherCarsInFront:
			closestCarInFront=min([otherCar for otherCar in otherCars if otherCar>0])*car.road.length
		else:
			closestCarInFront=float('inf')
		
		#Decelerate due to stop sign or red light
		if (stoppingDistance>=distanceToEnd-stopLine and signal in [roadsGraph.signal.stop, roadsGraph.signal.red] and not car.stopped):
			vehicle.decelerate(car,dt)
		
		#Decelerate due to traffic in front
		elif stoppingDistance>=closestCarInFront-bumper:
			vehicle.decelerate(car,dt,markAsStopped=False) #Stopping behind traffic does not count as stopping at stop sign

		#Stopped at stop sign. Check is road is clear
		elif car.stopped and car.speed==0 and signal==roadsGraph.signal.stop:
			roadsToWatch=[road for road in roadsGraph.roadsFromPoint(intersection,roads) if road!=car.road]
			CarsToWatch=[otherCar for otherCar in cars if otherCar.road in roadsToWatch and ((otherCar.road.pointB==intersection and otherCar.direction==vehicle.direction.AtoB) or (otherCar.road.pointA==intersection and otherCar.direction==vehicle.direction.BtoA))]
			stayPut=False
			for otherCar in CarsToWatch:
				otherCarDistanceToEnd, _, _ = vehicle.distanceToGo(otherCar)
				if otherCarDistanceToEnd/otherCar.speed < 3:
					stayPut=True
			if not stayPut:
				vehicle.accelerate(car,dt)

		#Accelerate to speed limit
		elif (stoppingDistance<distanceToEnd-stopLine or (signal==roadsGraph.signal.stop and car.stopped) or signal==roadsGraph.signal.green) and car.speed<car.road.speedLimit:
			vehicle.accelerate(car,dt)
		
		#end of the road
		if car.position>1 or car.position<0:
			newRoad=chooseNewRoad(car,intersection,roads)
			if not newRoad:
				cars.remove(car)
	return cars

