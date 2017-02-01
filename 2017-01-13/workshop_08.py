
# coding: utf-8

# ## House_Modeling

# ### [**Esempio**](http://www.bridgeofhopebarm.org/Content/img/building/floor_1.jpg)

# In[1]:

from larlib import *


# In[2]:

def getWalls(layerlines):
    """Draws walls'lines by reading pairs of points from file, and puts them in a single structure."""
    import csv
    reader = csv.reader(open(layerlines, 'r'),delimiter=',')
    lines = []
    struct = []
    for row in reader:
        lines.append([[eval(row[0]),eval(row[1])],[eval(row[2]),eval(row[3])]])
    for line in lines:
        struct.append(MKPOL([line,[[1,2]],None]))
    walls = STRUCT([struct[0],struct[1]])
    for i in range(2,len(struct)):
        walls = STRUCT([walls,struct[i]])
    return walls


# In[3]:

def getDoors(layerlines,walls):
	"""Draws doors'outlines by reading pairs of points from file.
	Every four lines read from the file, 2D rectangles are created in place of the doors with the JOIN function."""
	import csv
	reader = csv.reader(open(layerlines, 'r'),delimiter=',')
	lines = []
	doorSpacesArray = []
	doorsArray = []
	for row in reader:
		lines.append([[eval(row[0]),eval(row[1])],[eval(row[2]),eval(row[3])]])
	for i in xrange(0,len(lines),4):
		line1 = MKPOL([lines[i],[[1,2]],None])
		line2 = MKPOL([lines[i+1],[[1,2]],None])
		line3 = MKPOL([lines[i+2],[[1,2]],None])
		line4 = MKPOL([lines[i+3],[[1,2]],None])
		doorSpace = JOIN([STRUCT([line1,line2,line3,line4])])
		door = PROD([doorSpace,QUOTE([40])])
		door = OFFSET([1,1,1])(door)
		door = INTERSECTION([door,walls])
		sizes = SIZE([1,2])(door)
		if sizes[0]>sizes[1]:
			doorsArray.append(T([1,2])([UKPOL(door)[0][0][0],UKPOL(door)[0][0][1]])(buildDoor(sizes[0],sizes[1],41,1)))
		else:
			doorsArray.append(T([1,2])([UKPOL(door)[0][0][0]-sizes[0]/2.,UKPOL(door)[0][0][1]-sizes[1]])(buildDoor(sizes[0],sizes[1],41,2)))
		doorSpacesArray.append(doorSpace)
		i = i+4
	doorSpaces = STRUCT([doorSpacesArray[0],doorSpacesArray[1]])
	doors = STRUCT([doorsArray[0],doorsArray[1]])
	for i in range(2,len(doorSpacesArray)):
		doorSpaces = STRUCT([doorSpaces,doorSpacesArray[i]])
	for i in range(2,len(doorsArray)):
		doors = STRUCT([doors,doorsArray[i]])
	return [doors,doorSpaces]

def buildDoor(dx,dy,dz,axis):
	wood = Color4f(128/255.,30/255.,30/255.)
	darkWood = Color4f(94/255.,15/255.,15/255.)
	door = COLOR(wood)(CUBOID([dx,dy,dz]))
	if axis == 1:
		ornament = T([1,2,3])([dx*0.2-0.75,-0.1,dz*0.1])(SKEL_1(CUBOID([dx*0.6,0,dz*0.35])))
		offset = dy+0.2
	if axis == 2:
		ornament = T([1,2,3])([-0.1,dy*0.2-0.75,dz*0.1])(SKEL_1(CUBOID([0,dy*0.6,dz*0.35])))
		offset = dx+0.2
	ornament = COLOR(darkWood)(OFFSET([offset,offset,offset])(ornament))
	door = STRUCT([door,ornament,T(3)(dz*0.45-0.75),ornament])
	return door

# In[4]:

def getWindows(layerlines,walls):
	"""Draws windows'outlines by reading pairs of points from file.
	Every four lines read from the file, 2D rectangles are created in place of the doors with the JOIN function."""
	import csv
	reader = csv.reader(open(layerlines, 'r'),delimiter=',')
	lines = []
	windowSpaceArray = []
	windowsArray = []
	for row in reader:
		lines.append([[eval(row[0]),eval(row[1])],[eval(row[2]),eval(row[3])]])
	for i in xrange(0,len(lines),4):
		line1 = MKPOL([lines[i],[[1,2]],None])
		line2 = MKPOL([lines[i+1],[[1,2]],None])
		line3 = MKPOL([lines[i+2],[[1,2]],None])
		line4 = MKPOL([lines[i+3],[[1,2]],None])
		windowSpace = JOIN([STRUCT([line1,line2,line3,line4])])
		window = PROD([windowSpace,QUOTE([25])])
		window = OFFSET([1,1,1])(window)
		window = INTERSECTION([window,walls])
		sizes = SIZE([1,2])(window)
		if sizes[0]>sizes[1]:
			windowsArray.append(T([1,2])([UKPOL(window)[0][0][0]-sizes[0],UKPOL(window)[0][0][1]])(buildWindow(sizes[0],sizes[1],26,1)))
		else:
			windowsArray.append(T([1,2])([UKPOL(window)[0][0][0]-sizes[0]/2.,UKPOL(window)[0][0][1]-sizes[1]])(buildWindow(sizes[0],sizes[1],26,2)))
		windowSpaceArray.append(windowSpace)
		i = i+4
	windowSpaces = STRUCT([windowSpaceArray[0],windowSpaceArray[1]])
	windows = STRUCT([windowsArray[0],windowsArray[1]])
	for i in range(2,len(windowSpaceArray)):
		windowSpaces = STRUCT([windowSpaces,windowSpaceArray[i]])
	for i in range(2,len(windowsArray)):
		windows = STRUCT([windows,windowsArray[i]])
	return [windows,windowSpaces]

def buildWindow(dx,dy,dz,axis):
	window = CUBOID([dx,dy,dz])
	if axis == 1:
		panel = T([1,3])([dx*0.1,dz*0.1])(CUBOID([dx*0.35,dy+0.1,dz*0.35]))
		panels = STRUCT([panel,T(1)(dx*0.45)(panel)])
	if axis == 2:
		panel = T([2,3])([dy*0.1,dz*0.1])(CUBOID([dx+0.1,dy*0.35,dz*0.35]))
		panels = STRUCT([panel,T(2)(dy*0.45)(panel)])
	panels = STRUCT([panels,T(3)(dz*0.45)(panels)])
	window = STRUCT([window,panels])
	window = DIFF([window,panels])
	window = STRUCT([window,MATERIAL([0,0,1,1, 1,1,1,0.2, 0,0,0,1, 0,0,0,1, 50])(panels)])
	return window
	
def buildLateralPanels(layerlines):
    panels = []
    panels.append(MKPOL([[[263.6498107910156, 169.31765747070312, 0.0],[300.01531982421875, 207.7034912109375, 30.0],[300.01531982421875, 640.0487670898438, 30.0],[264.65997314453125, 680.4548950195312, 0.0]],[[1,2,3,4]],None]))
    panels.append(MKPOL([[[264.65997314453125, 680.4548950195312, 0.0],[300.01531982421875, 640.0487670898438, 30.0],[393.95947265625, 641.0589599609375, 30.0],[424.2640686035156, 680.4548950195312, 0.0]],[[1,2,3,4]],None]))
    panels.append(MKPOL([[[393.95947265625, 641.0589599609375, 30.0],[424.2640686035156, 680.4548950195312, 0.0],[393.9595031738281, 353.1654357910156, 30.0],[423.25390625, 393.5715637207031, 0.0]],[[1,2,3,4]],None]))
    panels.append(MKPOL([[[423.25390625, 393.5715637207031, 0.0],[393.9595031738281, 353.1654357910156, 30.0],[599.0204467773438, 353.1654357910156, 30.0],[565.6854248046875, 394.5816955566406, 0.0]],[[4,1,2,3]],None]))
    panels.append(MKPOL([[[565.6854248046875, 394.5816955566406, 0.0],[599.0204467773438, 353.1654357910156, 30.0],[599.0204467773438, 418.82537841796875, 30.0],[565.6854248046875, 473.37359619140625, 0.0]],[[1,2,3,4]],None]))
    panels.append(MKPOL([[[565.6854248046875, 473.37359619140625, 0.0],[599.0204467773438, 418.82537841796875, 30.0],[660.6397599999999,418.82536999999996, 30.0],[643.4671630859375, 473.37359619140625, 0.0]],[[1,2,3,4]],None]))
    panels.append(MKPOL([[[643.4671630859375, 473.37359619140625, 0.0],[660.6397599999999,418.82536999999996, 30.0],[659.629638671875, 448.1197814941406, 30.0],[643.4671699999999,496.60711, 0.0]],[[1,2,3,4]],None]))
    panels.append(MKPOL([[[643.4671699999999,496.60711, 0.0],[659.629638671875, 448.1197814941406, 30.0],[705.0864868164062, 448.1197814941406, 30.0],[731.3504399999999, 496.60711, 0.0]],[[1,2,3,4]],None]))
    panels.append(MKPOL([[[731.3504638671875, 496.60711669921875, 0.0],[705.0864868164062, 448.1197814941406, 30.0],[705.0864868164062, 418.82537841796875, 30.0],[731.3504638671875, 451.1502380371094, 0.0]],[[1,2,3,4]],None]))
    panels.append(MKPOL([[[731.3504638671875, 451.1502380371094, 0.0],[705.0864868164062, 418.82537841796875, 30.0],[758.6245727539062, 418.82537841796875, 30.0],[794.9900512695312, 451.1502380371094, 0.0]],[[1,2,3,4]],None]))
    panels.append(MKPOL([[[794.9900512695312, 451.1502380371094, 0.0],[758.6245727539062, 418.82537841796875, 30.0],[758.6245727539062, 353.1654357910156, 30.0],[794.9900512695312, 329.93194580078125, 0.0]],[[1,2,3,4]],None]))
    panels.append(MKPOL([[[794.9900512695312, 329.93194580078125, 0.0],[758.6245727539062, 353.1654357910156, 30.0],[694.9849243164062, 353.1654357910156, 30.0],[731.3504638671875, 329.93194580078125, 0.0]],[[1,2,3,4]],None]))
    panels.append(MKPOL([[[731.3504638671875, 329.93194580078125, 0.0],[694.9849243164062, 353.1654357910156, 30.0],[694.9849243164062, 208.71363830566406, 30.0],[731.3504638671875, 226.89639282226562, 0.0]],[[1,2,3,4]],None]))
    panels.append(MKPOL([[[731.3504638671875, 226.89639282226562, 0.0],[694.9849243164062, 208.71363830566406, 30.0],[817.2134399414062, 208.71363830566406, 30.0],[850.5484619140625, 226.89639282226562, 0.0]],[[1,2,3,4]],None]))
    panels.append(MKPOL([[[850.5484619140625, 226.89639282226562, 0.0],[817.2134399414062, 208.71363830566406, 30.0],[817.2134399414062, 135.982666015625, 30.0],[850.5484619140625, 122.85066986083984, 0.0]],[[1,2,3,4]],None]))
    panels.append(MKPOL([[[850.5484619140625, 122.85066986083984, 0.0],[817.2134399414062, 135.982666015625, 30.0],[691.9544677734375, 136.99281311035156, 30.0],[732.360595703125, 123.86083221435547, 0.0]],[[1,2,3,4]],None]))
    panels.append(MKPOL([[[732.360595703125, 123.86083221435547, 0.0],[691.9544677734375, 136.99281311035156, 30.0],[691.9544677734375, 88.50548553466797, 30.0],[732.360595703125, 47.0892333984375, 0.0]],[[1,2,3,4]],None]))
    panels.append(MKPOL([[[732.360595703125, 47.0892333984375, 0.0],[691.9544677734375, 88.50548553466797, 30.0],[691.9544677734375, 88.50548553466797, 30.0],[732.360595703125, 47.0892333984375, 0.0]],[[1,2,3,4]],None]))
    panels.append(MKPOL([[[732.360595703125, 47.0892333984375, 0.0],[691.9544677734375, 88.50548553466797, 30.0],[469.7209167480469, 88.50548553466797, 30.0],[424.2640686035156, 47.0892333984375, 0.0]],[[1,2,3,4]],None]))
    panels.append(MKPOL([[[424.2640686035156, 47.0892333984375, 0.0],[469.7209167480469, 88.50548553466797, 30.0],[469.7209167480469, 207.7034912109375, 30.0],[424.2640686035156, 169.31768798828125, 0.0]],[[1,2,3,4]],None]))
    panels.append(MKPOL([[[424.2640686035156, 169.31768798828125, 0.0],[469.7209167480469, 207.7034912109375, 30.0],[300.01531982421875, 207.7034912109375, 30.0],[263.6498107910156, 169.31765747070312, 0.0]],[[1,2,3,4]],None]))
    lateralPanels = STRUCT([panels[0],panels[1]])
    for i in range(2,len(panels)):
        lateralPanels = STRUCT([lateralPanels,panels[i]])
    return lateralPanels