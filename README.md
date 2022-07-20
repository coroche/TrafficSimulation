# Traffic Simulation
Exploring object oriented programming with a traffic simulator  
  
The aim of this project is to allow a user to create a map, define roads signals, add vehicles and have them interect with traffic signals and eachother. 

### GUI
With the GUI, users can define maps by placing points and connecting them with roads. Each road is defined with a speed limit and each end gets a traffic signal. Maps can also be saved for future use and loaded back into the GUI. Once the map is complete, the user selects a number of cars and clicks simulate.

![GUI](https://user-images.githubusercontent.com/49063400/180084282-5c700494-fabc-45d8-8b38-fdfe813a3d32.png)

### Output
Once the user clicks simulate an animation is created showing the selected number of cars interacting with their map. 

![traffic](https://user-images.githubusercontent.com/49063400/180085238-4039b848-9834-43e6-b475-eac7afe505e0.gif)

In the above animation we can see cars mostly moving freely at the speed limit, except at t-junctions where they have a stop sign. Here they come to a stop and only proceed once the way is clear.
