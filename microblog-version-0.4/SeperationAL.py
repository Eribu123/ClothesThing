
# import skimage
# from sklearn import datasets
from sklearn import svm
# from matplotlib import style
import numpy as np
import os
import time
from PIL import Image,ImageOps
# import Image
from sklearn.model_selection import train_test_split
from sklearn.cluster import KMeans
from collections import Counter
# from sklearn import model_selection
import waterShedTest
from sklearn.model_selection import GridSearchCV
import pickle
shirtPath='Users/Aubrey/Desktop/clothes/Shirts'
testPath = shirtPath+'ResizedShirts/' +'Apic_016.jpg'
# s=cv2.imread(testPath)
# print s
# time.sleep(50)

# import Utils

clothesPath='../../clothes/'
pantsPath='../../clothes/pants/'
grayPathShirt=shirtPath+"ResizedShirts/GrayShirts/"
grayPathPants=pantsPath+"ResizedPants/GrayPants/"
# desktop='../../'
numericData=[]
p=[]
mostusedColors=[]

def ResizeFolderOfImages(path,savePath):
	'''
	FUNCTION FOR RESIZING large amounts of images
'''
	for x,y,z in os.walk(path):
		for i in range(0,len(z)):
			if z[i] =='.DS_Store':
				continue
			# print z[i]
			s= Image.open(path +z[i], 'r')
			s.load()
			s= s.resize((150,150))
			# s.show()
			s.save(savePath+z[i])
def StandarizeImage(Input):
	s= Input
	s.load()
	s=s.resize((150,150))
	return s
# ResizeFolderOfImages(shirtPath,shirtPath+"ResizedShirts/")
# ResizeFolderOfImages(pantsPath,pantsPath+"ResizedPants/")

def GrayOut(path,finalPath):
	#GRAYS OUT A BUNCH FILES
	for x,y,z in os.walk(path):
		for i in range(0,len(z)):
			if z[i] =='.DS_Store':
				continue
			a=Image.open(path +z[i], 'r')
			# print 'fds'
			a=ImageOps.grayscale(a)

			# a.convert('LA')
			# print np.array(a)
			a.save(finalPath+z[i])

# GrayOut(pantsPath+'ResizedPants/',pantsPath+'ResizedPants/GrayPants/')
# GrayOut(shirtPath+'ResizedShirts/',shirtPath+'ResizedShirts/'+"GrayShirts/")

# -------------------------------------------

def CreateClassifer(shirtPath,pantsPath):
	'''
	intilized variables for temp use
	'''
	param_grid = [
  	{'C': [1, 10, 100, 1000], 'kernel': ['linear']},
 	{'C': [1, 10, 100, 1000], 'gamma': [0.001, 0.0001], 'kernel': ['rbf']},
 	]

	shirtLabels=[]
	pantsLabels=[]
	shirtsAr=[]
	pantsAr=[]

	# reads the data and stores them
	read_item_files(shirtPath,shirtLabels,shirtsAr)
	read_item_files(pantsPath,pantsLabels,pantsAr)
	# print pantsAr

	z=pantsAr+shirtsAr #turns all the arrays into array
	# print z
	for i in range(0,len(z)):
		z[i]= np.reshape(z[i],(1,z[i].shape[0]*z[i].shape[1])) #reshapes the array for use
		for j in range(0,len(z[i])):
			z[i]= z[i][j]
	# 		# reshapes it into 2d Array

	np.reshape(z,(1,-1))
	#gets the data lableed
	numericData=[0]*len(pantsLabels)
	numericData.extend([1]*len(shirtLabels))
	print len(numericData)



	X_train, X_test, y_train, y_test = train_test_split(
	z, numericData, test_size=0.4, random_state=0) #y represents the lables in numeric form




	clf = GridSearchCV(svm.SVC(C=1), param_grid, cv=5)

	clf.fit(X_train, y_train)


	#SVC creates a vector that will normally will creates a line of best fit.
	#But were using it to fit a line that fits around alll of the given plotted points.
	clf.fit(X_train,y_train)
	np.reshape(X_test,(-1,1))
	# print('prediction', clf.predict (X_test))
	# print(y_test)

	# print clf.score(X_test,y_test)

	return clf

#READIES THE ITEMS FOR THE CLASSIFER
def read_item_files(path,labels,Ar):
	x=[]; y=[];

	for x,y,z in os.walk(path):
		x=z[1:]

	for i in x:
		Ar.append(np.array(Image.open(path+i,'r')))
		labels.append(i)

def Cluster(Input):
	colors=[]
	data=np.array(Image.open(Input)) #READIES THE DATA
	markers=waterShedTest.Watershed(Input) #MARKS THE BACKGROUND
	clf=KMeans(n_clusters = 4, max_iter=10,n_init=1, random_state=1) #creates classifer
	#THE KMmeans classifer works by taking graphed points and finds the center of those points based off of their postion, we could somehting similar with our compass.
	data= np.reshape(data,(data.shape[1]*data.shape[0],3))#Resahapes into a 2d array


	markers=np.reshape(markers,(markers.shape[0]*markers.shape[1])) #RESHAPES THE MARKERS INTO A 1d array

	#Removes background:
	for i in range(0,len(markers)):
		if markers[i]>1:
			colors.append(data[i])

	clf.fit(colors)
	centroids=clf.cluster_centers_

	labels=clf.labels_
#LABELS CORRELATE TO THE CLUSTER THAT THE DATA FALLS UNDER EXAMPLE DATA[0] FALLS UNDER LABEL[0] AND CENTROID[0]
#CENTROIDS REPRESENT THE BEST COLOR

	colors = ['r','g','b','c','k','y','m']

	n_clusters= len(np.unique(labels))

	a=Counter(labels) #creates a dictionary of the colors most used
	# print centroids
	# print a[0], centroids[0]
	# print 'number of estimated clusters',n_clusters

	theColors=[]
	#loops through the array of centroids to find the largest centroid
	for i in range(0,len(centroids)):
		for j in a.most_common(2):
			if i==j[0]:
				theColors.append(centroids[i])


	print theColors

	return theColors

pathToClassifer='classifier.pkl'
def SaveClassifer(path):
	with open(path, 'wb+') as fid:
		pickle.dump(CreateClassifer(grayPathShirt,grayPathPants), fid)

# SaveClassifer(pathToClassifer)
def classify(Input):
	with open (pathToClassifer,'rb') as fid:
		clf=pickle.load(fid)
	Input=ImageOps.grayscale(Input)
	Input = StandarizeImage(Input)
	Input = np.array(Input)
	print Input
	print 1
	#Input = np.reshape(Input,(Input.shape[0]*Input.shape[1]))
	print Input
	# print('prediction', clf.predict (Input))
	return clf.predict(Input)
	# print(y_test)


def Score(Input):
	# Input = StandarizeImage(Input)
	itemIs=classify(Image.open(Input))
	colorsAre=Cluster(Input)
	# print 'scoring',itemIs, colorsAre
	return [itemIs, colorsAre]
