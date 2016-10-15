"""Creates simple parametric building structure."""

from larlib import *

dy=[8,5]
hz=[11,18,12]

def buildSpaceFrame(px,py,bx,bz):
	"""Creates and shows a space frame of reinforced concrete."""
	global dy
	global hz
	pillars = buildPillars(px,py,bz)
	beams = buildBeams(px,bx,bz)
	spaceFrame=STRUCT([pillars,beams])
	VIEW(spaceFrame)
	return spaceFrame

def buildPillars(px,py,bz):
	"""Creates pillars of the building's space frame."""
	x=[px]
	for i in dy:
		x.append(-i)
		x.append(px)
	y=[py]
	bases=PROD([QUOTE(x),QUOTE(y)])
	l=0
	for j in hz:
		pillars[l]=PROD([bases,QUOTE([j])])
		l=l+1
	allPillars=STRUCT([pillars[0],T(3)(hz[0]+bz),pillars[1]])
	allPillars=STRUCT([allPillars,T(3)(hz[0]+hz[1]+bz*2),pillars[2]])
	return allPillars

def buildBeams(px,bx,bz):
	"""Creates beams of the building's space frame."""
	x=[]
	for i in dy:
		x.append(i+px*2)
	y=[bx]
	bases=PROD([QUOTE(x),QUOTE(y)])
	beams=PROD([bases,QUOTE([bz])])
	beams=T(1)(-px/2)(beams)
	beams=T(3)(hz[0])(beams)
	allBeams=STRUCT([beams,T(3)(hz[1]+bz),beams])
	allBeams=STRUCT([allBeams,T(3)(hz[1]+hz[2]+bz*2),beams])
	return allBeams