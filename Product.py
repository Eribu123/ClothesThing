from __future__ import division

from collections import Counter
from PIL import Image
import numpy as np
import time
import timeit
import colorsys
import math
from matplotlib.colors import rgb_to_hsv
score=0
colors=[]
colorsHSV=[]
shirt = Image.open('images/shirtRed.png')
pants = Image.open('images/CyanPants.jpg')
shirtAr= np.array(shirt)
pantsAr= np.array(pants)



z=[]
c=[]

CompColors=[]
ratios=[]
ratio=0

# (4, 5, 6)
def GetMode(shirtAr,pantsAr):
	# print(len(array[0]),'\n yufiyu')

	# print(len(array))
	# print(array)

	# print(len(imgAr[0]))
	for i in range(0,len(shirtAr)):
		# for j in range(0,len(array[i])):
		jk = map(tuple,shirtAr[i])
		z.append(z.extend( tuple(jk)))
		# print(z)

	for i in range(0,len(pantsAr)):
		# for j in range(0,len(array[i])):
		jk = map(tuple,pantsAr[i])
		z.extend( tuple(jk))

	n=tuple(z)

	data = Counter(n)
	colors.extend(data.most_common())
	# print(data.most_common(),'dsdfas')   # Returns all unique items and their counts


# print(colorsys.rgb_to_hsv(1, 0, .78),'0')
# print(colorsys.rgb_to_hsv(0, 1, .2),'1')
# print(colorsys.hsv_to_rgb((.3666666666666667),1,1),'1Hsv')
# print(colorsys.hsv_to_rgb((.87),1,1),'2Hsv')
# y=[1,1,1,1,1,2,2,2,23,34,4]
def getCompliment(coll1, coll2):
	# currColorToCompare=()
	# GetMode(imgAr)
	
	
	# b=list(coll1[0])
	# b1=list(coll2[0])
	# print(coll1)
	# print('ds')
	a= list(map(lambda x:  x/255, coll1[0]))
	a1= list(map(lambda x:  x/255, coll2[0]))
	currColor=(colorsys.rgb_to_hsv(a[0],a[1],a[2]), coll1[1])
	currColor1=(colorsys.rgb_to_hsv(a1[0],a1[1],a1[2]), coll2[1])
	# print currColor, 'cur0',currColor1, 'cur1'
			# for eachColor in range(0,3):
	if currColor not in colorsHSV:
		colorsHSV.append(currColor)
	if currColor1 not in colorsHSV:
		colorsHSV.append(currColor1)
	# print currColor,'dsafasdfdnfa;lsdnfgi;oasgio'

	d= currColor1[0][0]-.5
	d1= currColor1[0][0]+.5

	if((currColor[0][2]!=0 and currColor[0][1]!=0) or (currColor1[0][1] != 0 and currColor1[0][2] != 0)): #because then it's black
		if( d-.1<= currColor[0][0]<= d+.1 or d1-.1 <= currColor[0][0]<=d1+.1):
			print 'complementary colors'
					# if currColor[0] not in CompColors:
			CompColors.append(currColor)
			CompColors.append(currColor1)
			ratio=currColor[1]/(currColor1[1]+currColor[1])
			ratios.append(ratio)
			# print(a)
			print CompColors, 'compColors'
			return CompColors

		else:
			print 'no comp'


	else:
		print	'no complement'
		# print(colors)

	return None

	# for z in CompColors:
		# sortedCompColors= max(lambda:  )
	# return CompColors


def giveOutput():
	#complementary
	GetMode(shirtAr,pantsAr)
 	# c=4/0
 	# print('sdf')

	for z in range(0, len(colors)):
		for x in range(z+1, len(colors)):
			c=getCompliment(colors[x], colors[z])
	for i in ratios:
		if(20<=i<=65):
			score -= i
	print(score)

giveOutput()
		
def checkDarkness():
	pass

