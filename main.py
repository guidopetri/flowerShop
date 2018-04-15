#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#python 3.6.4

#Flower Shop Ordering To Go - Create a flower shop application which deals in flower objects and use those flower objects in a bouquet object which can then be sold. Keep track of the number of objects and when you may need to order more.

from enum import Enum #so we can remain sane
import sys
#from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QDesktopWidget, QAction, qApp, QToolBar #GUI
#from PyQt5.QtCore import Qt
#from PyQt5.QtGui import QIcon
import PyQt5.QtWidgets
import PyQt5.QtCore
import PyQt5.QtGui
import random #for randomization functions
import json #for saving our settings

class Color(Enum):
	RED = 1
	GREEN = 2
	BLUE = 3
	YELLOW = 4
	WHITE = 5
	PURPLE = 6
	ORANGE = 7
	INDIGO = 8
	LILAC = 9
	PINK = 10
	GOLD = 11
	BLACK = 12

class Sizes(Enum):
	TINY = 1
	SMALL = 2
	MEDIUM = 3
	LARGE = 4
	HUGE = 5
	LEGENDARY = 6

class Flowers(Enum):
	ROSE = 1
	TULIP = 2
	SUNFLOWER = 3
	DAISY = 4
	MAGNOLIA = 5
	DAFFODIL = 6
	IRIS = 7
	CARNATION = 8
	JASMINE = 9
	LILY = 10
	CHERRY_BLOSSOM = 11
	PANSY = 12
	VIOLET = 13
	MARIGOLD = 14
	LILAC = 15
	POINSETTIA = 16
	CHRYSANTHEMUM = 17
	BLEEDING_HEART = 18
	BABYS_BREATH = 19
	POPPY = 20
	BLUEBELL = 21
	CAMOMILE = 22
	ZINNIA = 23
	COSMO = 24
	JACOBS_LADDER = 25
	RAFFLESIA = 26
	PASSIFLORA = 27
	DANDELION = 28
	GAYFEATHER = 29
	LOTUS = 30

class Months(Enum):
	JAN = 1
	FEB = 2
	MAR = 3
	APR = 4
	MAY = 5
	JUN = 6
	JUL = 7
	AUG = 8
	SEP = 9
	OCT = 10
	NOV = 11
	DEC = 12

class Weekdays(Enum):
	SUN = 1
	MON = 2
	TUE = 3
	WED = 4
	THU = 5
	FRI = 6
	SAT = 7

class Locations(Enum):
	SUBWAY = 1
	DOWNTOWN_STREET = 2
	SUBURBS_STREET = 3
	MALL = 4
	INTERNET = 5
	FESTIVAL = 6

class FlowerSpecies:
	def __init__(self,possibleColors,species,possibleSizes,lifespan,growMonths):
		self.possibleColors = possibleColors
		self.species = species
		self.possibleSizes = possibleSizes
		self.lifespan = lifespan
		self.growMonths = growMonths

class Flower:
	def __init__(self,price,color,flowerSpecies,size,age,ageRate):
		self.price = price
		if color in flowerSpecies.possibleColors:
			self.color = color
		else:
			raise ValueError('Color %s not allowed for flower species %s' % (color.name,flowerSpecies.species.name))
		self.flowerSpecies = flowerSpecies
		if size in flowerSpecies.possibleSizes:
			self.size = size
		else:
			raise ValueError('Size %s not allowed for flower species %s' % (size.name,flowerSpecies.species.name))
		self.age = age
		self.ageRate = ageRate
		self.alive = True

	def senesce(self):
		self.age += self.ageRate
		if self.age >= self.flowerSpecies.lifespan:
			self.alive = False

class Bouquet:
	def __init__(self,FlowersDict):
		self.flowers = FlowersDict
		self.price = 0
		for flower,count in self.flowers.items():
			self.price += count*flower.price
		self.age = max([flower.age for flower in self.flowers.keys()])
		self.alive = True

	def senesce(self):
		for flower in self.flowers.keys():
			flower.senesce()
			if flower.alive == False:
				self.alive = False
		self.age = max([flower.age for flower in self.flowers.keys()])

class flowerOrder:
	def __init__(self,bouquetDict,totalPrice,deliveryDate,beauty):
		self.bouquetDict = bouquetDict
		self.totalPrice = 0
		for bouquet,count in self.bouquetDict.items():
			self.totalPrice += count*bouquet.price
		self.deliveryDate = deliveryDate
		self.beauty = beauty
		self.alive = True

	def senesce(self):
		for bouquet in self.bouquetDict.keys():
			bouquet.senesce()
			if bouquet.alive == False:
				self.alive = False

class Shop:
	def __init__(self,flowerStock,stockPrices,location,flowerPrices,openingHours,openDays,employeesDict):
		self.flowerStock = flowerStock
		self.stockPrices = stockPrices
		self.location = location
		self.flowerPrices = flowerPrices
		self.openingHours = openingHours
		self.openDays = openDays
		self.employeesDict = employeesDict

class MainWindow(PyQt5.QtWidgets.QMainWindow):
	def __init__(self):
		super().__init__()
		self.init_UI()
		initFlowers()

	def init_UI(self):
		self.resize(800,600)
		self.center()
		self.setWindowTitle('flowerShop')
		exitAct = PyQt5.QtWidgets.QAction(PyQt5.QtGui.QIcon('media/images/exitIcon.png'),'Exit',self)
		exitAct.setShortcut('Ctrl+Q')
		exitAct.triggered.connect(PyQt5.QtWidgets.qApp.quit)

		self.toolbarFunctions = self.addToolBar('Functions')
		self.toolbarFunctions.setMovable(False)
		self.toolbarFunctions.addAction(exitAct)

		saveAct = PyQt5.QtWidgets.QAction(PyQt5.QtGui.QIcon('media/images/saveIcon.png'),'Save',self)
		saveAct.setShortcut('Ctrl+S')
		saveAct.triggered.connect(saveGame)

		self.toolbarFunctions.addAction(saveAct)

		shopViewAct = PyQt5.QtWidgets.QAction(PyQt5.QtGui.QIcon('media/images/shopIcon.png'),'Shop',self)
		shopViewAct.triggered.connect(viewShops)

		toolbarViews = PyQt5.QtWidgets.QToolBar('View',self)
		self.addToolBar(PyQt5.QtCore.Qt.LeftToolBarArea,toolbarViews)
		toolbarViews.setAllowedAreas(PyQt5.QtCore.Qt.LeftToolBarArea)
		toolbarViews.setMovable(False)
		toolbarViews.addAction(shopViewAct)

		bouquetViewAct = PyQt5.QtWidgets.QAction(PyQt5.QtGui.QIcon('media/images/bouquetIcon.png'),'Bouquet',self)
		bouquetViewAct.triggered.connect(viewBouquets)

		toolbarViews.addAction(bouquetViewAct)

		flowerViewAct = PyQt5.QtWidgets.QAction(PyQt5.QtGui.QIcon('media/images/flowerIcon.png'),'Flower',self)
		flowerViewAct.triggered.connect(viewFlowers)

		toolbarViews.addAction(flowerViewAct)

		overView(self)


	def center(self):
		qr = self.frameGeometry()
		cp = PyQt5.QtWidgets.QDesktopWidget().availableGeometry().center()
		qr.moveCenter(cp)
		self.move(qr.topLeft())

def initFlowers():
	Rose = FlowerSpecies([Color.RED],Flowers.ROSE,[Sizes.MEDIUM,Sizes.LARGE,Sizes.LEGENDARY],10,[Months.APR,Months.MAY,Months.JUN,Months.JUL,Months.AUG])
	Tulip = FlowerSpecies([Color.RED],Flowers.TULIP,[Sizes.MEDIUM,Sizes.LARGE,Sizes.LEGENDARY],10,[Months.APR,Months.MAY,Months.JUN,Months.JUL,Months.AUG])
	Sunflower = FlowerSpecies([Color.RED],Flowers.SUNFLOWER,[Sizes.MEDIUM,Sizes.LARGE,Sizes.LEGENDARY],10,[Months.APR,Months.MAY,Months.JUN,Months.JUL,Months.AUG])
	Daisy = FlowerSpecies([Color.RED],Flowers.DAISY,[Sizes.MEDIUM,Sizes.LARGE,Sizes.LEGENDARY],10,[Months.APR,Months.MAY,Months.JUN,Months.JUL,Months.AUG])
	Magnolia = FlowerSpecies([Color.RED],Flowers.MAGNOLIA,[Sizes.MEDIUM,Sizes.LARGE,Sizes.LEGENDARY],10,[Months.APR,Months.MAY,Months.JUN,Months.JUL,Months.AUG])
	Daffodil = FlowerSpecies([Color.RED],Flowers.DAFFODIL,[Sizes.MEDIUM,Sizes.LARGE,Sizes.LEGENDARY],10,[Months.APR,Months.MAY,Months.JUN,Months.JUL,Months.AUG])
	Iris = FlowerSpecies([Color.RED],Flowers.IRIS,[Sizes.MEDIUM,Sizes.LARGE,Sizes.LEGENDARY],10,[Months.APR,Months.MAY,Months.JUN,Months.JUL,Months.AUG])
	Carnation = FlowerSpecies([Color.RED],Flowers.CARNATION,[Sizes.MEDIUM,Sizes.LARGE,Sizes.LEGENDARY],10,[Months.APR,Months.MAY,Months.JUN,Months.JUL,Months.AUG])
	Jasmine = FlowerSpecies([Color.RED],Flowers.JASMINE,[Sizes.MEDIUM,Sizes.LARGE,Sizes.LEGENDARY],10,[Months.APR,Months.MAY,Months.JUN,Months.JUL,Months.AUG])
	Lily = FlowerSpecies([Color.RED],Flowers.LILY,[Sizes.MEDIUM,Sizes.LARGE,Sizes.LEGENDARY],10,[Months.APR,Months.MAY,Months.JUN,Months.JUL,Months.AUG])
	Cherry_Blossom = FlowerSpecies([Color.RED],Flowers.CHERRY_BLOSSOM,[Sizes.MEDIUM,Sizes.LARGE,Sizes.LEGENDARY],10,[Months.APR,Months.MAY,Months.JUN,Months.JUL,Months.AUG])
	Pansy = FlowerSpecies([Color.RED],Flowers.PANSY,[Sizes.MEDIUM,Sizes.LARGE,Sizes.LEGENDARY],10,[Months.APR,Months.MAY,Months.JUN,Months.JUL,Months.AUG])
	Violet = FlowerSpecies([Color.RED],Flowers.VIOLET,[Sizes.MEDIUM,Sizes.LARGE,Sizes.LEGENDARY],10,[Months.APR,Months.MAY,Months.JUN,Months.JUL,Months.AUG])
	Marigold = FlowerSpecies([Color.RED],Flowers.MARIGOLD,[Sizes.MEDIUM,Sizes.LARGE,Sizes.LEGENDARY],10,[Months.APR,Months.MAY,Months.JUN,Months.JUL,Months.AUG])
	Lilac = FlowerSpecies([Color.RED],Flowers.LILAC,[Sizes.MEDIUM,Sizes.LARGE,Sizes.LEGENDARY],10,[Months.APR,Months.MAY,Months.JUN,Months.JUL,Months.AUG])
	Poinsettia = FlowerSpecies([Color.RED],Flowers.POINSETTIA,[Sizes.MEDIUM,Sizes.LARGE,Sizes.LEGENDARY],10,[Months.APR,Months.MAY,Months.JUN,Months.JUL,Months.AUG])
	Chrysanthemum = FlowerSpecies([Color.RED],Flowers.CHRYSANTHEMUM,[Sizes.MEDIUM,Sizes.LARGE,Sizes.LEGENDARY],10,[Months.APR,Months.MAY,Months.JUN,Months.JUL,Months.AUG])
	Bleeding_Heart = FlowerSpecies([Color.RED],Flowers.BLEEDING_HEART,[Sizes.MEDIUM,Sizes.LARGE,Sizes.LEGENDARY],10,[Months.APR,Months.MAY,Months.JUN,Months.JUL,Months.AUG])
	Babys_Breath = FlowerSpecies([Color.RED],Flowers.BABYS_BREATH,[Sizes.MEDIUM,Sizes.LARGE,Sizes.LEGENDARY],10,[Months.APR,Months.MAY,Months.JUN,Months.JUL,Months.AUG])
	Poppy = FlowerSpecies([Color.RED],Flowers.POPPY,[Sizes.MEDIUM,Sizes.LARGE,Sizes.LEGENDARY],10,[Months.APR,Months.MAY,Months.JUN,Months.JUL,Months.AUG])
	Bluebell = FlowerSpecies([Color.RED],Flowers.BLUEBELL,[Sizes.MEDIUM,Sizes.LARGE,Sizes.LEGENDARY],10,[Months.APR,Months.MAY,Months.JUN,Months.JUL,Months.AUG])
	Camomile = FlowerSpecies([Color.RED],Flowers.CAMOMILE,[Sizes.MEDIUM,Sizes.LARGE,Sizes.LEGENDARY],10,[Months.APR,Months.MAY,Months.JUN,Months.JUL,Months.AUG])
	Zinnia = FlowerSpecies([Color.RED],Flowers.ZINNIA,[Sizes.MEDIUM,Sizes.LARGE,Sizes.LEGENDARY],10,[Months.APR,Months.MAY,Months.JUN,Months.JUL,Months.AUG])
	Cosmo = FlowerSpecies([Color.RED],Flowers.COSMO,[Sizes.MEDIUM,Sizes.LARGE,Sizes.LEGENDARY],10,[Months.APR,Months.MAY,Months.JUN,Months.JUL,Months.AUG])
	Jacobs_Ladder = FlowerSpecies([Color.RED],Flowers.JACOBS_LADDER,[Sizes.MEDIUM,Sizes.LARGE,Sizes.LEGENDARY],10,[Months.APR,Months.MAY,Months.JUN,Months.JUL,Months.AUG])
	Rafflesia = FlowerSpecies([Color.RED],Flowers.RAFFLESIA,[Sizes.MEDIUM,Sizes.LARGE,Sizes.LEGENDARY],10,[Months.APR,Months.MAY,Months.JUN,Months.JUL,Months.AUG])
	Passiflora = FlowerSpecies([Color.RED],Flowers.PASSIFLORA,[Sizes.MEDIUM,Sizes.LARGE,Sizes.LEGENDARY],10,[Months.APR,Months.MAY,Months.JUN,Months.JUL,Months.AUG])
	Dandelion = FlowerSpecies([Color.RED],Flowers.DANDELION,[Sizes.MEDIUM,Sizes.LARGE,Sizes.LEGENDARY],10,[Months.APR,Months.MAY,Months.JUN,Months.JUL,Months.AUG])
	Gayfeather = FlowerSpecies([Color.RED],Flowers.GAYFEATHER,[Sizes.MEDIUM,Sizes.LARGE,Sizes.LEGENDARY],10,[Months.APR,Months.MAY,Months.JUN,Months.JUL,Months.AUG])
	Lotus = FlowerSpecies([Color.RED],Flowers.LOTUS,[Sizes.MEDIUM,Sizes.LARGE,Sizes.LEGENDARY],10,[Months.APR,Months.MAY,Months.JUN,Months.JUL,Months.AUG])
	return

def calculateAgeTest():
	Rose = FlowerSpecies([Color.RED],Flowers.ROSE,[Sizes.TINY,Sizes.LEGENDARY],16,Months.DEC)
	Daisy = FlowerSpecies([Color.GREEN],Flowers.DAISY,[Sizes.TINY],22,Months.DEC)
	Flower1 = Flower(1,Color.RED,Rose,Sizes.LEGENDARY,15,random.randint(1,2))
	Flower2 = Flower(1,Color.GREEN,Daisy,Sizes.TINY,20,random.randint(1,2))
	dictFlowers = {Flower1:3,Flower2:2}
	bouquet1 = Bouquet(dictFlowers)
	print(bouquet1.age)
	bouquet1.senesce()
	print(bouquet1.age)
	print(bouquet1.alive)
	return

def saveGame():
	pass

def viewShops():
	pass

def viewBouquets():
	pass

def viewFlowers():
	pass

def overView(window):
	btn1 = PyQt5.QtWidgets.QPushButton('Calculate Age')
	btn1.clicked.connect(calculateAgeTest)
	btn2 = PyQt5.QtWidgets.QPushButton('Quit')
	btn2.clicked.connect(PyQt5.QtWidgets.QApplication.instance().quit)

	hbox = PyQt5.QtWidgets.QHBoxLayout()
	hbox.addStretch(1)
	hbox.addWidget(btn1)
	hbox.addWidget(btn2)

	vbox = PyQt5.QtWidgets.QVBoxLayout()
	vbox.addStretch(1)
	vbox.addLayout(hbox)

	mainWidget = PyQt5.QtWidgets.QWidget(window)
	mainWidget.setLayout(vbox)
	window.setCentralWidget(mainWidget)

	window.show()

def createFlower():
	pass

def createBouquet():
	pass

def foundShop():
	pass

random.seed()

app = PyQt5.QtWidgets.QApplication(sys.argv)
ex = MainWindow()

app.exec()