from __future__ import division
import colorsys
import SeperationAL as Al
# import numpy as np
import time
from PIL import Image
import pickle
pantsTestPath='../../../clothes/pants/ResizedPants/pic_349.jpg'
shirtTestPath='../../../clothes/shirts/ResizedShirts/' +'shirt_044.jpg'
# testPath = shirtPath+'ResizedShirts/' +'Apic_016.jpg'
# testPath1 = shirtPath+'ResizedShirts/' +'Apic_016.jpg'

savePath='Data.pkl'
# shirtImageDB=[]
# shirtColorDB=[]

# pantsImageDB=[]
# pantsColorDB=[]
needClothesToCompare='Please Input more clothes to compare'
def rgb2ryb(r,g,b):
	white = min(r,g,b)
	r = r - white
	g = g - white
	b = b - white
	maxg = max(r,g,b)
	yellow = min(r,g)
	r = r - yellow
	g = g - yellow
	if(b > 0 and g > 0):
		b = b / 2
		g = g / 2
	yellow = yellow + g
	b = b + g
	maxyellow = max(r,yellow,b)
	if(maxyellow > 0):
		r = r * maxg / maxyellow
		yellow = yellow * maxg / maxyellow
		b = b * maxg / maxyellow
	r = r + white
	yellow = yellow + white
	b = b + white
	return (r,yellow,b)

def color2ryb(color):
	return rgb2ryb(color[0],color[1],color[2])

def scorer(shirtb,pantb,shirtsc,pantsc):
	r,y,b = color2ryb(shirtb)
	shirtbase = colorsys.rgb_to_hsv(r/255.,y/255.,b/255.)
	r,y,b = color2ryb(pantb)
	pantbase = colorsys.rgb_to_hsv(r/255.,y/255.,b/255.)
	r,y,b = color2ryb(shirtsc)
	shirtsec = colorsys.rgb_to_hsv(r/255.,y/255.,b/255.)
	r,y,b = color2ryb(pantsc)
	pantsec = colorsys.rgb_to_hsv(r/255.,y/255.,b/255.)
	sbpb = min(abs(pantbase[0] - shirtbase[0]),(abs(pantbase[0] - (1-shirtbase[0]))))
	sbss = min(abs(shirtsec[0] - shirtbase[0]),(abs(shirtsec[0] - (1-shirtbase[0]))))
	sbps = min(abs(pantsec[0] - shirtbase[0]),(abs(pantsec[0] - (1-shirtbase[0]))))
	ssps = min(abs(pantbase[0] - shirtbase[0]),(abs(pantbase[0] - (1-shirtbase[0]))))
	sspb = min(abs(shirtsec[0] - shirtbase[0]),(abs(shirtsec[0] - (1-shirtbase[0]))))
	pbps = min(abs(pantsec[0] - shirtbase[0]),(abs(pantsec[0] - (1-shirtbase[0]))))
	shirtbave = (shirtb[0]+shirtb[1]+shirtb[2])/3.
	pantbave = (pantb[0]+pantb[1]+pantb[2])/3.
	shirtscave = (shirtsc[0]+shirtsc[1]+shirtsc[2])/3.
	pantscave = (pantsc[0]+pantsc[1]+pantsc[2])/3.
	sbpbscr = 50 - sbpb*100
	sspbscr = 20 - sspb*40
	sbpsscr = 10 - sbps*20
	sbssscr = 10 - sbss*20
	sspsscr = 5 - ssps*10
	pbpsscr = 5 - pbps*10	
	if(((shirtb[0] - shirtbave)**2 + (shirtb[1] - shirtbave)**2 + (shirtb[2] - shirtbave)**2) / 2) < 1600:
		sbpbscr = 50
		sbssscr = 10
		sbpsscr = 10
	if(((pantb[0] - pantbave)**2 + (pantb[1] - pantbave)**2 + (pantb[2] - pantbave)**2) / 2) < 1600:
		sbpbscr = 50
		sspbscr = 20
		pbpsscr = 5
	if(((shirtsc[0] - shirtscave)**2 + (shirtsc[1] - shirtscave)**2 + (shirtsc[2] - shirtscave)**2) / 2) < 1600:
		sbssscr = 10
		sspbscr = 20
		sspsscr = 5
	if(((pantsc[0] - pantscave)**2 + (pantsc[1] - pantscave)**2 + (pantsc[2] - pantscave)**2) / 2) < 1600:
		sbpsscr = 10
		sspsscr = 5
		pbpsscr = 5
	score = pbpsscr+sspsscr+sbssscr+sbpsscr+sspbscr+sbpbscr
	print '\n score: ',score
	return score

	
# print score
# Add Comment
COLORS=[]
def GetColors(Input1,Input2):
	COLORS=[]
	TheColors.append(Al.getColors(Input1))
	TheColors.append(Al.scgetColorsore(Input2))
	return TheColors

def saveImage(Input1,Input2,path):
	# print 'dsfs'

	open(savePath, 'wb+').close() #deletes all existing info on pickle file
	l=[]
	TheColors=Al.getColors(Input1)
	l.append(Image.open(Input1))
	l.append(TheColors)
	COLORS.append(TheColors)
	TheColors=Al.getColors(Input2)

	l.append(Image.open(Input2))
	l.append(TheColors)
	COLORS.append(TheColors)
	# print COLORS

	# print "\n the l:" ,l

	with open(savePath, 'a') as fid:
		pickle.dump(l, fid) 
		# print l
		
# saveImage(shirtTestPath,pantsTestPath,savePath) 

def loadData(path):
	with open(path,'rb') as fid:
	 	theData= pickle.load(fid)
	 	if len(theData)<=2:
	 		return False
	return theData
def runScorer(path):
	data=loadData(path)
	# print '\ndata',data
	if data != False:
		ShirtColors=data[1]
		PantsColors=data[3]

		a=	scorer(ShirtColors[1][0],ShirtColors[1][1], PantsColors[1][0],PantsColors[1][1])
		# print a
	else:
		return False



# runScorer(savePath)


# 1 Comment Collapse