import numpy as np
import cv2
from PIL import Image
# path = '/Users/Aubrey/Desktop/clothes/Shirts/ResizedShirts/testShirt.jpg'
def Watershed(Input):
	data = Input
	img = cv2.imread(Input)
	# print img
	img = cv2.GaussianBlur(img,(5,5),0)
	# print img
	gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	# gray= 255-gray
	ret, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
	# noise removal
	kernel = np.ones((3,3),np.uint8)
	# print thresh
	opening = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel, iterations = 2)
	# sure background area
	sure_bg = cv2.dilate(opening,kernel,iterations=3)
	# Finding sure foreground area
	dist_transform = cv2.distanceTransform(opening,cv2.DIST_L2,5)
	ret, sure_fg = cv2.threshold(dist_transform,0.7*dist_transform.max(),255,0)
	# Finding unknown region
	sure_fg = np.uint8(sure_fg)
	unknown = cv2.subtract(sure_bg,sure_fg)
	# a=cv2.subtract(a,sure_bg)
	# Marker labelling
	ret, markers = cv2.connectedComponents(sure_fg)

	# print 'forground'
	# print 'background'
	# Add one to all labels so that sure background is not 0, but 1
	markers = markers+1
	# Now, mark the region of unknown with zero
	markers[unknown==255] = 0

	markers = cv2.watershed(img,markers)
	#Marks the boundaries 
	img[markers == -1] = [255,0,0]

	return markers