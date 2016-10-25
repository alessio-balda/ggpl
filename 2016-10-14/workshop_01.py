"""Creates simple parametric building structure."""

from larlib import *

def buildSpaceFrame(px,py,bx,bz,dy,hz):
	"""Creates and shows a space frame of reinforced concrete."""
	pillars = buildPillars(px,py,bz,dy,hz)
	beams = buildBeams(px,bx,bz,dy,hz)
	pillars=COLOR(RED)(pillars)
	beams=COLOR(BLUE)(beams)
	spaceFrame=STRUCT([pillars,beams])
	VIEW(spaceFrame)
	return spaceFrame


def buildPillars(px,py,bz,dy,hz):
	"""Creates pillars of the building's space frame."""
	x = [px]
	for i in dy:
		x.append(-i)
		x.append(px)
	y = [py]
	bases = PROD([QUOTE(x),QUOTE(y)])
	l=0
	for j in hz:
		pillars[l]=PROD([bases,QUOTE([j])])
		l=l+1
	z=hz[0]
	allPillars=STRUCT([pillars[0],T(3)(z+bz),pillars[1]])
	for i in range(1,len(hz)-1):
		z=z+hz[i]
		allPillars=STRUCT([allPillars,T(3)([z+bz*(i+1)]),pillars[i+1]])
	return allPillars

def buildBeams(px,bx,bz,dy,hz):
	"""Creates beams of the building's space frame."""
	x=[]
	for i in dy:
		x.append(i+px*2)
	y=[bx]
	bases=PROD([QUOTE(x),QUOTE(y)])
	beams=PROD([bases,QUOTE([bz])])
	beams=T(1)(-px/2)(beams)
	beams=T(3)(hz[0])(beams)
	z=0
	allBeams=beams
	for i in range(1,len(hz)):
		z=z+hz[i]
		allBeams=STRUCT([allBeams,T(3)(z+bz*i),beams])
	return allBeams
		