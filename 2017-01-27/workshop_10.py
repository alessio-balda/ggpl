
# coding: utf-8

# ## Design of parametric multistorey house

# ### [**Esempio**](https://im.proptiger.com/2/5241970/12/presidency-flora-lower-level-duplex-plan-5bhk-6t-4325-sq-ft-552285.jpeg)

# In[1]:

from larlib import *


# In[2]:

from workshop_08 import *


# In[3]:

def zRotate(hpc,angle):
    """Rotate and object of type hpc around the z axys."""
    box=BOX([1,2,3])(hpc)
    size = SIZE([1,2,3])(box)
    return R([1,2])(angle)(T([1,2])([-size[0]/2.,-size[1]/2.])(hpc))


# In[4]:

def readFile(filename):
    """Read a file between filename."""
    import csv
    file = open(filename, 'rb')
    reader = csv.reader(file, delimiter=",")
    return reader


# In[5]:

def buildRoof(wallLines,roofLines):
    """Builds a roof by reading two lists of lines."""
    reader = readFile(wallLines)
    reader2 = readFile(roofLines)
    lines = []
    lines2 = []
    struct = []
    struct2 = []
    
    for row in reader:
        lines.append([[eval(row[0]),eval(row[1])],[eval(row[2]),eval(row[3])]])
    for line in lines:
        struct.append(MKPOL([line,[[1,2]],None]))
    bottom = STRUCT([struct[0],struct[1]])
    for i in range(2,len(struct)):
        bottom = STRUCT([bottom,struct[i]])
        
    for row in reader2:
        lines2.append([[eval(row[0]),eval(row[1])],[eval(row[2]),eval(row[3])]])
    for line in lines2:
        struct2.append(MKPOL([line,[[1,2]],None]))
    top = STRUCT([struct2[0],struct2[1]])
    for i in range(2,len(struct2)):
        top = STRUCT([top,struct2[i]])
    
    bottom = SOLIDIFY(bottom)
    top = T(3)(30)(TEXTURE(["wallTexture.jpg",TRUE, TRUE, 1, 1, 0, 10, 10])(SOLIDIFY(top)))
    lateralPanels = TEXTURE(["TextureRoof.jpg",TRUE, TRUE, 1, 1, 0, 10, 10])(buildLateralPanels(roofLines))
    return STRUCT([bottom,top,lateralPanels])


# In[6]:

def getStairs(layerlines):
    """Gets the space in which there will be placed the stairs."""
    reader = readFile(layerlines)
    lines = []
    stairSpacesArray = []
    for row in reader:
        lines.append([[eval(row[0]),eval(row[1])],[eval(row[2]),eval(row[3])]])
    for i in xrange(0,len(lines),4):
        line1 = MKPOL([lines[i],[[1,2]],None])
        line2 = MKPOL([lines[i+1],[[1,2]],None])
        line3 = MKPOL([lines[i+2],[[1,2]],None])
        line4 = MKPOL([lines[i+3],[[1,2]],None])
        stairSpace = JOIN([STRUCT([line1,line2,line3,line4])])
    return stairSpace


# In[7]:

def buildStairs(stairSpace):
    """Builds stairs in the space given as the parameter."""
    sizes = SIZE([1,2])(stairSpace)
    dz = 27.5
    a=dz/10
    nSteps=int(round(dz/a))
    sx=sizes[0]/nSteps/2
    sy=sizes[1]/2.
    sz=dz/nSteps
    stairs=CUBOID([sx,sy,sz*nSteps])
    for i in range(1,nSteps):
        stairs=STRUCT([stairs,T([1])([sx*i]),CUBOID([sx,sy,sz*(nSteps-i)])])
    stairs = STRUCT([stairs,T([1,2,3])([sizes[0]/4.,sy*1.5,dz]),zRotate(stairs,PI)])
    stairs = STRUCT([T(3)(1)(stairs),T(1)(-sizes[0]/2),CUBOID([sizes[0]/2,sizes[1],dz+1])])
    stairs = STRUCT([stairs,T([2])([sy])(CUBOID([sizes[0]/2,sy,dz+2]))])
    stairs = MATERIAL([0,0,1,1, 1,1,1,1, 0,0,1,0, 0,0,0,1, 100])(stairs)
    pillar = CUBOID([1,1,15])
    railing1 = pillar
    railing2 = pillar
    for i in range(1,int(round(sizes[0]/2))):
        railing1 = STRUCT([railing1,T(1)(2*i),pillar])
    railing1 = T([1,2,3])([-sizes[0]/2,-2,57])(railing1)
    for i in range(1,int(round(sizes[1]/4))):
        railing2 = STRUCT([railing2,T(2)(2*i),pillar])
    railing2 = T([1,2,3])([-sizes[0]/2,-1,57])(railing2)
    railing = STRUCT([railing1,T(1)(sizes[0]),railing2])
    stairs = STRUCT([stairs,railing,T([1,2,3])([-sizes[0]/2,-2,72]),CUBOID([sizes[0],1,1]),T(1)(sizes[0])(CUBOID([1,sizes[1]/2,1]))])
    stairs = T([1,2])([UKPOL(stairSpace)[0][0][0]-sizes[0]/2,UKPOL(stairSpace)[0][0][1]-sizes[1]])(stairs)
    return stairs


# In[8]:

cube = MATERIAL([0,0,1,1, 0.5,0.5,0,0.5, 0,0,0,0, 0,0,0,0, 50])(CUBOID([1,1,1]))


# In[9]:

def buildFloor(extWallsLines,intWallsLines,doorsLines,windowsLines,stairLines):
    """Creates a floor with walls, doors and windows, and keeps empty the room for the stairs."""
    extWalls = getWalls(extWallsLines)
    intWalls = getWalls(intWallsLines)
    floor = PROD([SOLIDIFY(extWalls),QUOTE([1])])
    walls = STRUCT([extWalls,intWalls])
    walls = PROD([walls,QUOTE([55])])
    walls = OFFSET([1,1,1])(walls)
    doorsParam = getDoors(doorsLines,walls)
    doorsSpace = doorsParam[1]
    doorsSpace = PROD([doorsSpace,QUOTE([40])])
    doorsSpace = OFFSET([1,1,1])(doorsSpace)
    windowsParam = getWindows(windowsLines,walls)
    windowsSpace = windowsParam[1]
    windowsSpace = PROD([windowsSpace,QUOTE([25])])
    windowsSpace = OFFSET([1,1,1])(windowsSpace)
    windows = windowsParam[0]   
    windows = T(3)(15)(windows)
    doors = doorsParam[0]  
    house = STRUCT([walls,doorsSpace,T(3)(15)(windowsSpace)])
    house = DIFF([house,doorsSpace])
    house = DIFF([house,T(3)(15)(windowsSpace)])
    house = MATERIAL([0,0,1,1, 1,1,1,1, 0,0,1,0, 0,0,0,1, 100])(house)  
    stairSpace = T([1,2])([-2,2])(getStairs(stairLines))
    stairSpace = PROD([stairSpace,QUOTE([2])])
    floor = STRUCT([floor,stairSpace])
    floor = TEXTURE(["TextureFloor.jpg",TRUE, TRUE, 1, 1, 0, 10, 10])(DIFF([floor,stairSpace]))
    house = STRUCT([house,floor,doors,windows])
    return house


# In[10]:

def buildHouse(extWallsLines,intWallsLines,doorsLines,windowsLines,stairLines,roofLines):
    """Builds a whole house of two floors, with a roof and the main door"""
    floor1 = buildFloor(extWallsLines,intWallsLines,doorsLines,windowsLines,stairLines)
    floorHeight = SIZE(3)(BOX([1,2,3])(floor1))
    floor2 = T(3)(floorHeight)(floor1)
    stairSpace = getStairs(stairLines)
    stairs = buildStairs(stairSpace)
    mainDoor = T([1,2])([731.351,266.9])(buildDoor(1.5,30,45,2))
    floor1 = STRUCT([floor1,mainDoor])
    roof=T(3)(floorHeight*2)(buildRoof(extWallsLines,roofLines))
    return STRUCT([floor1,floor2,stairs,roof])
