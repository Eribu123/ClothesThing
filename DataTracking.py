from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import sqlite3
import ScoringAl as SA
import SeperationAL as SepAl
import time
from PIL import Image
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 

conn=sqlite3.connect('DataBase.db')
c=conn.cursor()
# numberToIncrement = 0ResizedShirts ResizedPants
Spath1 = '/Users/Aubrey/Desktop/clothes/Shirts/ResizedShirts/TestShirt1.jpg'

Ppath1='/Users/Aubrey/Desktop/clothes/pants/ResizedPants/TestPants1.jpg'

Spath2 = '/Users/Aubrey/Desktop/clothes/Shirts/ResizedShirts/TestShirt2.jpg'

Ppath2='/Users/Aubrey/Desktop/clothes/pants/ResizedPants/TestPants2.jpg'

Spath3 = '/Users/Aubrey/Desktop/clothes/Shirts/ResizedShirts/TestShirt3.jpg'

Ppath3='/Users/Aubrey/Desktop/clothes/pants/ResizedPants/TestPants3.jpg'

Spath4 = '/Users/Aubrey/Desktop/clothes/Shirts/ResizedShirts/TestShirt4.jpg'

Ppath4='/Users/Aubrey/Desktop/clothes/pants/ResizedPants/TestPants4.jpg'

Spath5 = '/Users/Aubrey/Desktop/clothes/Shirts/ResizedShirts/TestShirt5.jpg'

Ppath5='/Users/Aubrey/Desktop/clothes/pants/ResizedPants/TestPants5.jpg'

score=0
def AddToUserInputData(ThisUser,ThisEmail,Uinput,Utype): #These are what were going to be getting from front end everytime the usr uses the product
	# score=0 
	# print _input

	c.execute("CREATE TABLE IF NOT EXISTS UserInputTable(id Integer PRIMARY KEY, usr Text, email Text, Input Text ,ClotheType Integer)")
	c.execute("INSERT INTO UserInputTable (usr,email,Input,ClotheType) VALUES (?,?,?,?)", (ThisUser,ThisEmail,Uinput,Utype))

	c.execute("SELECT Input from UserInputTable")

	for  i in c.fetchall():
		pass
		# print 'sdfasdfasdfasd',i
	c.execute("CREATE TABLE IF NOT EXISTS ScoreTable(id Integer PRIMARY KEY, UserName Text, Input1 Text, Input2 Text ,Score Integer)" )
	# for i in c.fetchall():
		#"create table %s (%s text,%s text)" % ("my_table","first","second") print i

	c.execute("SELECT Input from UserInputTable where usr=(?)", (ThisUser,))
	pantsType=[]
	shirtsType=[]
	x=0
	z=0
	for row in c.fetchall():
		x+=1
		# print 'x',x
		# print '\n',row[0],ThisUser,'\n'
		print row[0]
		if row[0]  != None:
			if SepAl.classify (Image.open(row[0])) ==1:
				shirtsType.append(row[0])
			elif SepAl.classify(Image.open(row[0]))==0:
				pantsType.append(row[0]) 
			# print 'pantsType',pantsType,ThisUser
			# print 'ShirtType',shirtsType,ThisUser
	print len(shirtsType)>0 , len(pantsType)>0
	if len(shirtsType)>0 and len(pantsType)>0:
		for aShirt  in shirtsType:
			for aPairPants in pantsType:
				z+=1
				# print 'z: ', z
				score=SA.scorer(SepAl.Cluster(aShirt)[0],SepAl.Cluster(aShirt)[1],SepAl.Cluster(aPairPants)[0],SepAl.Cluster(aPairPants)[1])
				# print 'fetchall: ', c.fetchall()
				c.execute("SELECT Input1, Input2, UserName from ScoreTable where Input1 =? and Input2=? and UserName =?" ,(aShirt,aPairPants,ThisUser))
				a=c.fetchone()
				if not a:
					c.execute("INSERT INTO ScoreTable (UserName,Input1,Input2,Score) VALUES (?,?,?,?)", (ThisUser,aShirt,aPairPants, score))



		# return score
	# c.execute("DELETE FROM USER")

	conn.commit()

def InputData(user,email,Input,Utype):
	

	# CreateUserReferenceTable(user)
	AddToUserInputData(user,email,Input,Utype)
c.execute("DROP TABLE ScoreTable")
c.execute("DROP TABLE UserInputTable")
InputData('ex1','j@gmail.com',Spath5,SepAl.classify(Image.open(Spath5))[0])
InputData('ex1','j@gmail.com',Ppath5,SepAl.classify(Image.open(Ppath5))[0])
InputData('ex2','j@gmail.com',Spath4,SepAl.classify(Image.open(Spath4))[0])
InputData('ex2','j@gmail.com',Ppath4,SepAl.classify(Image.open(Ppath4))[0])
InputData('ex3','j@gmail.com',Spath3,SepAl.classify(Image.open(Spath3))[0])
InputData('ex3','j@gmail.com',Ppath3,SepAl.classify(Image.open(Ppath3))[0])
InputData('ex4','j@gmail.com',Spath2,SepAl.classify(Image.open(Spath2))[0])
InputData('ex4','j@gmail.com',Ppath2,SepAl.classify(Image.open(Ppath2))[0])
InputData('ex5','j@gmail.com',Spath1,SepAl.classify(Image.open(Spath1))[0])
InputData('ex5','j@gmail.com',Ppath1,SepAl.classify(Image.open(Ppath1))[0])
print SepAl.classify(Image.open(Spath5))

conn.close()
# c.execute("INSERT INTO UserInputTable (id, user, email, imgPath, type )VALUE(0,'admin', 'test@gmail.com', 'path','-1' ) ")
