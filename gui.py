import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog as fd
from tkinter import ttk
import roadsGraph
import math, pickle
from pprint import pprint
from enum import Enum





class mode(Enum):
    point = 1
    road = 2
    delete = 3
    edit = 4


class MainApplication(tk.Frame):
	def __init__(self, parent, *args, **kwargs):

		self.parent = parent
		self.appFrame = tk.Frame(self.parent, bd=1, relief=tk.SOLID)
		self.appFrame.pack(fill=tk.BOTH, expand = True)


		self.pointRad = 8
		self.minD = 20
		self.drawMode = mode.point
		self.roadStart = None
		self.scale=1

		self.points = []
		self.roads = []

		self.currentFile=None
		self.changed=False
		self.moved=False
		self.editroad=None

		self.parent.geometry("1000x600")
		self.parent.title("Road Builder")

		self.parent.protocol("WM_DELETE_WINDOW", self.close)
		self.parent.bind('<Control-w>', self.close_noSave)
		self.parent.bind('<Control-n>', self.clearAll)
		self.parent.bind('<Control-o>', self.load)
		self.parent.bind('<Control-s>', self.save)
		self.parent.bind('<Control-S>', self.saveAs)
		self.parent.bind('<Escape>', self.esc)
		self.parent.bind('<Up>', self.up)
		self.parent.bind('<Down>', self.down)

		#Remove
		self.parent.bind('<space>', self.debug)

		self.menubar = tk.Menu(self.parent)
		self.filemenu = tk.Menu(self.menubar, tearoff=0)
		self.filemenu.add_command(label="New", command=self.clearAll, accelerator="Ctrl+N")
		self.filemenu.add_command(label="Open...", command=self.load, accelerator="Ctrl+O")
		self.filemenu.add_command(label="Save", command=self.save, accelerator="Ctrl+S")
		self.filemenu.add_command(label="Save As...", command=self.saveAs, accelerator="Ctrl+Shift+S")
		self.filemenu.add_separator()
		self.filemenu.add_command(label="Exit", command=self.close)
		self.menubar.add_cascade(label="File", menu=self.filemenu)


		self.canvas = tk.Canvas(self.appFrame, bg='lightsteelblue' )
		self.canvas.grid(row = 0, column = 1, sticky = 'nsew', rowspan=2)
		self.appFrame.grid_columnconfigure(1, weight=1)
		self.appFrame.grid_rowconfigure(0, weight=1)
		self.canvas.bind("<ButtonRelease-1>", self.unclick)
		self.canvas.bind("<MouseWheel>", self.zoom)
		self.canvas.bind("<ButtonPress-1>", self.scroll_start)
		self.canvas.bind("<B1-Motion>", self.scroll_move)


		self.drawGrid(self.canvas,50)

		btn_width = 10
		self.controls = tk.Frame(self.appFrame)
		self.controls.grid(row = 0, column = 0, sticky = 'n')

		#Parameters
		self.params_fr = tk.Frame(self.controls)
		self.params_fr.pack(padx=5, pady=25)

		self.speedLimit_lbl = tk.Label(self.params_fr, text='Speed Limit:')
		self.speedLimit_lbl.grid(row=0, column=0, sticky='e')

		self.speedLimit = tk.IntVar()
		self.speedLimit.set(30)
		self.speedLimit_sb = tk.Spinbox(self.params_fr,from_=0, to=50, width=3, textvariable=self.speedLimit)
		self.speedLimit_sb.grid(row=0, column=1, sticky='w')

		self.startSignal_lbl = tk.Label(self.params_fr, text='Start Signal:')
		self.startSignal_lbl.grid(row=1, column=0, sticky='e')

		self.startSignal = tk.StringVar()
		self.startSignal.set('Green')
		self.startSignal_cb = ttk.Combobox(self.params_fr, values=[s.name.capitalize() for s in roadsGraph.signal], width=5, state="readonly", textvariable=self.startSignal)
		self.startSignal_cb.grid(row=1, column=1, sticky='w')

		self.endSignal_lbl = tk.Label(self.params_fr, text='End Signal:')
		self.endSignal_lbl.grid(row=2, column=0, sticky='e')

		self.endSignal = tk.StringVar()
		self.endSignal.set('Green')
		self.endSignal_cb = ttk.Combobox(self.params_fr, values=[s.name.capitalize() for s in roadsGraph.signal], width=5, state="readonly", textvariable=self.endSignal)
		self.endSignal_cb.grid(row=2, column=1, sticky='w')




		#Mode Buttons
		self.modeButtons_fr = tk.Frame(self.controls)
		self.modeButtons_fr.pack(padx=5, pady=5)

		self.point_btn = tk.Button(self.modeButtons_fr, text = 'Point', command = self.pointMode, width = btn_width, relief='sunken')
		self.point_btn.pack(padx=2, pady=2)

		self.road_btn = tk.Button(self.modeButtons_fr, text  = 'Road', command = self.roadMode, width = btn_width)
		self.road_btn.pack(padx=2, pady=2)

		self.delete_btn = tk.Button(self.modeButtons_fr, text  = 'Delete', command = self.deleteMode, width = btn_width)
		self.delete_btn.pack(padx=2, pady=2)


		#Sim Controls
		self.simControls_fr = tk.Frame(self.controls)
		self.simControls_fr.pack(padx=5, pady=25)

		self.carCount_lbl = tk.Label(self.simControls_fr, text='No. of Cars:')
		self.carCount_lbl.grid(row=0, column=0, sticky='e')

		self.carCount = tk.IntVar()
		self.carCount.set(1)
		self.carCount_sb = tk.Spinbox(self.simControls_fr,from_=0, to=100, width=3, textvariable=self.carCount)
		self.carCount_sb.grid(row=0, column=1, sticky='w')

		self.sim_btn = tk.Button(self.simControls_fr, text  = 'Simulate', command = self.simulate, width = btn_width)
		self.sim_btn.grid(row=1, column=0, padx=5, pady=5, columnspan=2)


		#Instructions
		self.instruct = tk.Label(self.appFrame, text = 'Add points.\nConnect points with roads.\nClick simulate.')
		self.instruct.grid(row=1, column=0, padx=5, pady=5, sticky='s')

		self.mode_str = tk.StringVar()
		self.mode_str.set('Click to place a point')
		self.mode_lbl = tk.Label(self.appFrame, textvariable = self.mode_str)
		self.mode_lbl.grid(row = 0, column = 1, sticky = 'ne')

		self.parent.config(menu=self.menubar)

	#called when a user clicks anywhere on the canvas
	def unclick(self, event):
		#map window coordinates of the click to grid coordinates accounting for pan and zoom
		event.x = self.canvas.canvasx(event.x)/self.scale
		event.y = self.canvas.canvasy(event.y)/self.scale
		
		#if the user has not clicked and dragged to pan the canvas (i.e. clicked and released on the same location)
		if not self.moved:
			
			#Point mode
			if self.drawMode == mode.point:

				#round curser coordinates to snap to grid
				event.x, event.y = 50*round(event.x/50), 50*round(event.y/50)
				if [True for point in self.points if self.dist(point,event)<self.minD]:
					#if there is already a point there, do nothing
					return
				else:
					#draw a point, add it to points list and note that a change has been made
					p = self.drawPoint(event,'black')
					self.points.append(roadsGraph.point(event.x,event.y,p))
					self.changed=True

			#Road Mode
			elif self.drawMode in [mode.road, mode.edit] :

				#search for existing point or road at the click location
				point = [point for point in self.points if self.dist(point,event)<self.pointRad]
				road = [road for road in self.roads if self.pointOnRoad(road,event)]
				
				#if the click was on a point
				if point:
					point = point[0]

					#if a road was being edited exit edit mode and return to road mode
					if self.drawMode == mode.edit:
						self.leaveEditMode()
						self.drawMode = mode.road
					
					#if a road start point hasn't already been selected, mark this point as roadstart
					if not self.roadStart:
						self.canvas.tag_raise(point.cnvObj) #keep point on top of roads
						self.canvas.itemconfig(point.cnvObj, fill='blue') #highlight point
						self.roadStart = point
						self.mode_str.set('Select an end point for your road')
					
					#else add a road from the start point to this point
					else:
						#if the road doesn't already exits and the same point hasn't been selected for start and end
						if not [road for road in self.roads if road.pointA in [self.roadStart,point] and road.pointB in [self.roadStart,point]] and not self.roadStart == point:	
							
							#draw road and append objects to roads list
							startSignal_enum = roadsGraph.signal[self.startSignal.get().lower()]
							endSignal_enum = roadsGraph.signal[self.endSignal.get().lower()]

							r, s, e = self.drawRoad(self.roadStart, point, startSignal_enum, endSignal_enum)
							self.roads.append(roadsGraph.road(self.roadStart, point, startSignal_enum, endSignal_enum, self.speedLimit.get(), cnvObj=r, cnvObj_Start=s, cnvObj_End=e))
							self.changed=True

						#clear details of first click
						self.canvas.itemconfig(self.roadStart.cnvObj, fill='black')
						self.roadStart = None
						self.mode_str.set('Select a start point for your road, or select an existing road to edit')
				
				#if the click was on a road enter edit mode
				elif road and not self.roadStart:

					#if already in edit mode switch to new road in edit mode 
					if self.drawMode == mode.edit:
						if road[0] == self.editroad:
							self.leaveEditMode() #if the same road is selected again exit edit mode
							self.drawMode = mode.road
							return
						else:
							self.canvas.itemconfig(self.editroad.cnvObj, fill='black')
					
					#Set parameters to show the road's current settings
					self.drawMode = mode.edit
					self.editroad = road[0]
					self.canvas.itemconfig(self.editroad.cnvObj, fill='blue') #highlight road
					self.mode_str.set('Change road parameters')
					self.speedLimit.set(self.editroad.speedLimit)
					self.startSignal.set(self.editroad.endAtype.name.capitalize())
					self.endSignal.set(self.editroad.endBtype.name.capitalize())

					#set a trace for the paramter inputs to update the road when they are changed
					self.speedLimit.trace_id = self.speedLimit.trace('w',self.editSpeed)
					self.startSignal.trace_id = self.startSignal.trace('w',self.editStart)
					self.endSignal.trace_id = self.endSignal.trace('w',self.editEnd)	


			#delete mode
			elif self.drawMode == mode.delete:
				
				#search for existing point or road at the click location
				point = [point for point in self.points if self.dist(point,event)<self.pointRad]
				road = [road for road in self.roads if self.pointOnRoad(road,event)]
				
				#if the click was on a point
				if point:
					point = point[0]

					#gather all roads associated with the point and delete them
					attachedRoads = [road for road in self.roads if point in [road.pointA, road.pointB]]
					for road in list(attachedRoads):
						self.canvas.delete(road.cnvObj)
						self.canvas.delete(road.cnvObj_Start)
						self.canvas.delete(road.cnvObj_End)
						self.roads.remove(road)
					
					#delete the point
					self.canvas.delete(point.cnvObj)
					self.points.remove(point)
					self.changed=True
				
				#if the click was on a road
				elif road:

					#delete the road
					road = road[0]
					self.canvas.delete(road.cnvObj)
					self.canvas.delete(road.cnvObj_Start)
					self.canvas.delete(road.cnvObj_End)
					self.roads.remove(road)
					self.changed=True


	def dist(self, point1,point2):
		
		#Calculate the distance between two points
		dx = point2.x-point1.x
		dy = point2.y-point1.y
		return math.sqrt(dx**2+dy**2)

	def pointMode(self):

		#enter point mode

		#if moving from edit mode clear edit selection
		if self.drawMode == mode.edit:
			self.leaveEditMode()

		#set buttons/messages to show current mode
		self.drawMode = mode.point
		self.mode_str.set('Click to place a point')
		self.point_btn.config(relief='sunken')
		self.road_btn.config(relief='raised')
		self.delete_btn.config(relief='raised')
		
		#if a start point is selected for a road forget it
		if self.roadStart:
			self.canvas.itemconfig(self.roadStart.cnvObj, fill='black')
			self.roadStart = None



	def roadMode(self):

		#enter road mode
		
		#if moving from edit mode clear edit selection
		if self.drawMode == mode.edit:
			self.leaveEditMode()

		#set buttons/messages to show current mode
		self.drawMode = mode.road
		self.mode_str.set('Select a start point for your road, or select an existing road to edit')
		self.point_btn.config(relief='raised')
		self.road_btn.config(relief='sunken')
		self.delete_btn.config(relief='raised')

		#if a start point is selected for a road forget it
		if self.roadStart:
			self.canvas.itemconfig(self.roadStart.cnvObj, fill='black')
			self.roadStart = None


	def deleteMode(self):

		#enter delete mode

		#if moving from edit mode clear edit selection
		if self.drawMode == mode.edit:
			self.leaveEditMode()

		#set buttons/messages to show current mode
		self.drawMode = mode.delete
		self.mode_str.set('Select a road or point to delete')
		self.point_btn.config(relief='raised')
		self.road_btn.config(relief='raised')
		self.delete_btn.config(relief='sunken')

		#if a start point is selected for a road forget it
		if self.roadStart:
			self.canvas.itemconfig(self.roadStart.cnvObj, fill='black')
			self.roadStart = None


	#functions called when parameter inputs are changed while in edit mode
	def editSpeed(self, a,b,c):
		#set the selected road's speed
		self.editroad.speedLimit = int(self.speedLimit.get())

	def editStart(self, a,b,c):
		#set the selected road's start signal and update canvas object to reflect this
		self.editroad.endAtype = roadsGraph.signal[self.startSignal.get().lower()]
		sCol = roadsGraph.signalColours[self.startSignal.get().lower()]	
		self.canvas.itemconfig(self.editroad.cnvObj_Start, fill=sCol)	

	def editEnd(self, a,b,c):
		#set the selected road's end signal and update canvas object to reflect this
		self.editroad.endBtype = roadsGraph.signal[self.endSignal.get().lower()]
		eCol = roadsGraph.signalColours[self.endSignal.get().lower()]
		self.canvas.itemconfig(self.editroad.cnvObj_End, fill=eCol)


	def esc(self, event):
		#when the escape key is pressed exit edit mode and forget road start points

		if self.drawMode == mode.edit:
			self.leaveEditMode()
			self.drawMode = mode.road
		if self.roadStart:
			self.canvas.itemconfig(self.roadStart.cnvObj, fill='black')
			self.roadStart = None


	def leaveEditMode(self):
		#unhighlight selected road and delete traces on input parameters

		self.canvas.itemconfig(self.editroad.cnvObj, fill='black')
		self.editroad = None
		self.speedLimit.trace_vdelete('w', self.speedLimit.trace_id)
		self.startSignal.trace_vdelete('w', self.startSignal.trace_id)
		self.endSignal.trace_vdelete('w', self.endSignal.trace_id)


	def clearAll(self, event=None):
		#clears the current canvas 
		#if unsaved changes prompt use to save them
		if self.changed:
			if self.points and self.querySave('New Map','There are unsaved changes to this map.\nDo you want to save it before loading another?'):
				self.canvas.delete('all')
				self.drawGrid(self.canvas,50)
				self.points.clear()
				self.roads.clear()
		else:
			self.canvas.delete('all')
			self.drawGrid(self.canvas,50)
			self.points.clear()
			self.roads.clear()

	def drawGrid(self, canvas, line_distance):
		#create grid on canvas
		#vertical lines
		canvas_width = 1000
		canvas_height = 600
		for x in range(-10*canvas_width,11*canvas_width,line_distance):
			canvas.create_line(x, -10*canvas_height, x, 11*canvas_height, fill='cornflowerblue')
		#horizontal lines
		for y in range(-10*canvas_height,11*canvas_height,line_distance):
			canvas.create_line(-10*canvas_width, y, 11*canvas_width, y, fill='cornflowerblue')

	def drawPoint(self, point,fill):
		#draw a circle of radius pointRad at point with colour fill
		x1, y1 = self.scale*(point.x - self.pointRad), self.scale*(point.y - self.pointRad)
		x2, y2 = self.scale*(point.x + self.pointRad), self.scale*(point.y + self.pointRad)
		p = self.canvas.create_oval(x1, y1, x2, y2, fill=fill)

		#return the object for inclusion in the points list
		return p


	def drawRoad(self, start, end, startSignal, endSignal):
		#draw a line of thickness 1.8*pointRad from start to end. Add coloured segments at ends to signify signal type
		
		#end colours
		sCol = roadsGraph.signalColours[startSignal.name]
		eCol = roadsGraph.signalColours[endSignal.name]

		#adjust point positions to scale
		startx, starty, endx, endy = start.x*self.scale, start.y*self.scale, end.x*self.scale, end.y*self.scale
		dirVect = [25*(endx - startx)/self.dist(start,end), 25*(endy - starty)/self.dist(start,end)]
		
		#draw lines
		r = self.canvas.create_line(startx, starty, endx, endy, width=1.8*self.pointRad*self.scale)
		s = self.canvas.create_line(startx, starty, startx+dirVect[0], starty+dirVect[1], width=1.8*self.pointRad*self.scale, fill=sCol)
		e = self.canvas.create_line(endx, endy, endx-dirVect[0], endy-dirVect[1], width=1.8*self.pointRad*self.scale, fill=eCol)
		
		#raise points above road end signal colours
		self.canvas.tag_raise(start.cnvObj)
		self.canvas.tag_raise(end.cnvObj)
		
		#return road and end marker objects for inclusion in roads list
		return r,s,e





	def close(self):
		#close window without simulating
		#ask to save unsaved changes
		if self.changed and self.querySave('Exit','There are unsaved changes to this map.\nDo you want to save it before exiting?'):
			self.parent.destroy()
			exit()
		self.parent.destroy()
		exit()


	def close_noSave(self, event):
		#close window without saving or simulating
		self.parent.destroy()
		exit()


	def pointOnRoad(self, road,point):
		#returns true if point is on road
		x0, y0 = road.pointA.x, road.pointA.y
		x1, y1 = road.pointB.x, road.pointB.y

		#if road insn't vertical (infinite slope)
		if x1 != x0:

			#line equation for road
			m = (y1-y0)/(x1-x0)
			c = y0-m*x0
			#point is within half the road thickness of the line (equivalent to sqrt(m**2+1) tolerance on y) and is between the end points
			if abs(point.y-(m*point.x+c))<.9*self.pointRad*math.sqrt(m**2+1) and point.x not in [min(point.x,x0,x1), max(point.x,x0,x1)] and (m == 0 or point.y not in [min(point.y,y0,y1), max(point.y,y0,y1)]):
				return True		
		else:
			#vertical line
			if abs(point.x-x0)<.9*self.pointRad and point.y not in [min(point.y,y0,y1) ,max(point.y,y0,y1)]:
				return True	
		return False



	def querySave(self, title,message):
		qSave = messagebox.askyesnocancel(title=title, message=message)
		if qSave is None:
			return False
		elif qSave:
			if not self.save():
				return False
		return True

	def simulate(self):
		if not self.roads:
			messagebox.showerror(title='Error', message='Place some roads before simulating')
			return

		if self.changed:
			if self.querySave('Simulate','There are unsaved changes to this map.\nDo you want to save it before simulating?'):
				self.parent.destroy()
		else:
			self.parent.destroy()

	def save(self, event=None, initialfile='NewMap.p'):

		roadMap = [self.points,self.roads]

		if self.currentFile:
			filename = self.currentFile
		else: 
			file = fd.asksaveasfile(initialfile = initialfile, defaultextension=".p",filetypes=[("Pickled Objects","*.p"),("All Files","*.*")])
			if not file:
				return False
			elif not file.name[-2:] == '.p':
				filename = file.name + '.p'
			else:
				filename = file.name
		
		pickle.dump( roadMap, open( filename, "wb" ) )
		self.currentFile = filename
		self.changed=False
		return True

	def saveAs(self, event=None):

		initialfile=self.currentFile
		self.currentFile=None
		if initialfile:
			initialfile=initialfile[initialfile.rfind('/')+1:]
			self.save(initialfile='CopyOf_'+initialfile)
		else:
			self.save()


	def load(self, event=None):

		self.clearAll()
		f = fd.askopenfilename(filetypes=[("Pickled Objects","*.p"),("All Files","*.*")])
		if not f:
			return
		self.loadFile(f)

	def loadFile(self, f):

		try:
			roadMap = pickle.load( open( f, "rb" ) )
		except:
			tk.messagebox.showerror(title='Error', message='Could not open file')
			return
		self.points, self.roads = roadMap[0], roadMap[1]
		self.currentFile = f
		for point in self.points:
			p = self.drawPoint(point,'black')
			point.cnvObj = p
		for road in self.roads:
			r, s, e = self.drawRoad(road.pointA, road.pointB, road.endAtype, road.endBtype)
			road.cnvObj = r
			road.cnvObj_Start = s
			road.cnvObj_End = e



	def scroll_start(self, event):

		self.canvas.scan_mark(event.x, event.y)
		self.moved=False

	def scroll_move(self, event):

		self.canvas.scan_dragto(event.x, event.y, gain=1)
		self.moved=True

	def zoom(self, event):

		event.x = self.canvas.canvasx(event.x)
		event.y = self.canvas.canvasy(event.y)
		if (event.delta > 0):
			self.canvas.scan_mark(round(event.x*1.1), round(event.y*1.1))
			self.canvas.scan_dragto(round(event.x),round(event.y), gain=1)
			self.canvas.scale("all", 0, 0, 1.1, 1.1)
			self.scale *= 1.1

		elif (event.delta < 0):
			self.canvas.scan_mark(round(event.x/1.1), round(event.y/1.1))
			self.canvas.scan_dragto(round(event.x),round(event.y), gain=1)
			self.canvas.scale("all", 0, 0, 1/1.1, 1/1.1)
			self.scale *= 1/1.1
		
		for road in self.roads:
			self.canvas.itemconfig(road.cnvObj, width = self.scale*1.8*self.pointRad)
			self.canvas.itemconfig(road.cnvObj_Start, width = self.scale*1.8*self.pointRad)
			self.canvas.itemconfig(road.cnvObj_End, width = self.scale*1.8*self.pointRad)

	def up(self, event):
		if self.drawMode == mode.point:
			self.deleteMode()
		elif self.drawMode == mode.road:
			self.pointMode()
		elif self.drawMode == mode.delete:
			self.roadMode()

	def down(self, event):
		if self.drawMode == mode.point:
			self.roadMode()
		elif self.drawMode == mode.road:
			self.deleteMode()
		elif self.drawMode == mode.delete:
			self.pointMode()

	#remove
	def debug(self, event):
		print(self.editroad.theta)



# def design(f=None):
# 	if f:
# 		print(f)
# 		self.loadFile(f)
# 	tk.mainloop()
# 	return points, roads, carCount.get()

def main(currentFile=None):
	root = tk.Tk()
	designApp = MainApplication(root)
	if currentFile:
		designApp.loadFile(currentFile)
	root.mainloop()
	return designApp.points, designApp.roads, designApp.carCount.get(), designApp.currentFile

if __name__ == "__main__":
	main()