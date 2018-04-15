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
	LOTUS = 0
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

class Account:
	def __init__(self,money,ShopCollection):
		self.money = money
		self.ShopCollection = ShopCollection

class MainWindow(PyQt5.QtWidgets.QMainWindow):
	def __init__(self,money):
		super().__init__()
		self.flowerSpeciesList = initFlowers()
		self.money = money
		self.init_UI()

	def init_UI(self):
		self.resize(800,600)
		self.center()
		self.setWindowTitle('flowerShop')

		#create toolbars
		toolbarFunctions = PyQt5.QtWidgets.QToolBar('Functions',self)
		self.addToolBar(PyQt5.QtCore.Qt.TopToolBarArea,toolbarFunctions)
		toolbarFunctions.setAllowedAreas(PyQt5.QtCore.Qt.TopToolBarArea)
		toolbarFunctions.setMovable(False)

		toolbarViews = PyQt5.QtWidgets.QToolBar('View',self)
		self.addToolBar(PyQt5.QtCore.Qt.LeftToolBarArea,toolbarViews)
		toolbarViews.setAllowedAreas(PyQt5.QtCore.Qt.LeftToolBarArea)
		toolbarViews.setMovable(False)

		#create actions
		exitAct = PyQt5.QtWidgets.QAction(PyQt5.QtGui.QIcon('media/images/exitIcon.png'),'Exit',self)
		exitAct.setShortcut('Ctrl+Q')
		exitAct.triggered.connect(PyQt5.QtWidgets.qApp.quit)

		saveAct = PyQt5.QtWidgets.QAction(PyQt5.QtGui.QIcon('media/images/saveIcon.png'),'Save',self)
		saveAct.setShortcut('Ctrl+S')
		saveAct.triggered.connect(saveGame)

		shopViewAct = PyQt5.QtWidgets.QAction(PyQt5.QtGui.QIcon('media/images/shopIcon.png'),'Shop',self)
		shopViewAct.triggered.connect(viewShops)

		overViewAct = PyQt5.QtWidgets.QAction(PyQt5.QtGui.QIcon('media/images/overviewIcon.png'),'Overview',self)
		overViewAct.triggered.connect(lambda:overView(self))

		bouquetViewAct = PyQt5.QtWidgets.QAction(PyQt5.QtGui.QIcon('media/images/bouquetIcon.png'),'Bouquet',self)
		bouquetViewAct.triggered.connect(viewBouquets)

		flowerViewAct = PyQt5.QtWidgets.QAction(PyQt5.QtGui.QIcon('media/images/flowerIcon.png'),'Flower',self)
		flowerViewAct.triggered.connect(viewFlowers)

		#add actions to toolbars
		toolbarFunctions.addAction(exitAct)
		toolbarFunctions.addAction(saveAct)

		toolbarViews.addAction(overViewAct)
		toolbarViews.addAction(shopViewAct)
		toolbarViews.addAction(bouquetViewAct)
		toolbarViews.addAction(flowerViewAct)

		#main overview screen
		overView(self)

	def center(self):
		qr = self.frameGeometry()
		cp = PyQt5.QtWidgets.QDesktopWidget().availableGeometry().center()
		qr.moveCenter(cp)
		self.move(qr.topLeft())

def initFlowers():
	Lotus = FlowerSpecies([Color.RED],Flowers.LOTUS,[Sizes.MEDIUM,Sizes.LARGE,Sizes.LEGENDARY],10,[Months.APR,Months.MAY,Months.JUN,Months.JUL,Months.AUG])
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
	flowersList = [Lotus,Rose,Tulip,Sunflower,Daisy,Magnolia,Daffodil,Iris,Carnation,Jasmine,Lily,Cherry_Blossom,Pansy,Violet,Marigold,Lilac,Poinsettia,Chrysanthemum,Bleeding_Heart,Babys_Breath,Poppy,Bluebell,Camomile,Zinnia,Cosmo,Jacobs_Ladder,Rafflesia,Passiflora,Dandelion,Gayfeather]
	return flowersList

def nextDay(account,moneyLabel,inventoryLabel):
	for shop in account.ShopCollection:
		for flower in shop.flowerStock:
			if random.randint(1,100) > 50:
				account.money+=flower.price
				shop.flowerStock.remove(flower)
			else:
				flower.senesce()
		moneyLabel.setText('Money: %s'%str(account.money))
		list1=[]
		for flower in account.ShopCollection[0].flowerStock:
			list1.append(flower.flowerSpecies.species)
		inventoryLabel.setText('Inventory: %s'%list1)
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
	Shop1 = Shop([],[],Locations.SUBWAY,[],[],[],{})
	mainAccount = Account(5,[Shop1])
	#create buttons
	btn1 = PyQt5.QtWidgets.QPushButton('Next Day')
	btn1.clicked.connect(lambda:nextDay(mainAccount,moneyLabel,inventoryLabel))
	btn2 = PyQt5.QtWidgets.QPushButton('Quit')
	btn2.clicked.connect(PyQt5.QtWidgets.QApplication.instance().quit)
	moneyLabel = PyQt5.QtWidgets.QLabel('Money: %s'%str(mainAccount.money))
	list1 = []
	for flower in mainAccount.ShopCollection[0].flowerStock:
		list1.append(flower.flowerSpecies.species)
	inventoryLabel = PyQt5.QtWidgets.QLabel('Inventory: %s'%list1)
	#flowerCreateButton1 = PyQt5.QtWidgets.QPushButton('Buy Rose Flower')
	#flowerCreateButton1.clicked.connect(lambda:createFlower(window.flowerSpeciesList,Flowers.ROSE,moneyLabel))
	#flowerCreateButton2 = PyQt5.QtWidgets.QPushButton('Buy Tulip Flower')
	#flowerCreateButton2.clicked.connect(lambda:createFlower(window.flowerSpeciesList,Flowers.TULIP,moneyLabel))

	flowerCombo = PyQt5.QtWidgets.QComboBox(window)
	flowerCombo.addItems([str(item.species.name) for item in window.flowerSpeciesList])

	buyButton = PyQt5.QtWidgets.QPushButton('Buy')
	buyButton.clicked.connect(lambda:createFlower(window.flowerSpeciesList,flowerCombo.currentText(),mainAccount,moneyLabel,inventoryLabel))

	#create grid and add widgets
	grid = PyQt5.QtWidgets.QGridLayout()

	grid.addWidget(moneyLabel,1,0)
	grid.addWidget(inventoryLabel,0,2)
	#grid.addWidget(flowerCreateButton1,1,1)
	grid.addWidget(flowerCombo,3,1)
	grid.addWidget(buyButton,3,2)
	#grid.addWidget(flowerCreateButton2,1,2)
	grid.addWidget(btn1,2,1)
	grid.addWidget(btn2,2,2)

	mainWidget = PyQt5.QtWidgets.QWidget(window)
	mainWidget.setLayout(grid)
	window.setCentralWidget(mainWidget)

	window.show()

def createFlower(flowerSpeciesList,flowerTypeStr,account,moneyLabel,inventoryLabel):
	for flower in Flowers:
		if flower.name == flowerTypeStr:
			flowerType = flower
	if account.money > 0:
		account.money -= 1
		moneyLabel.setText('Money: %s'%str(account.money))
		flower1 = Flower(2.5,Color.RED,flowerSpeciesList[flowerType.value],Sizes.MEDIUM,random.randint(1,5),random.randint(1,3))
		account.ShopCollection[0].flowerStock.append(flower1)
		list1=[]
		for flower in account.ShopCollection[0].flowerStock:
			list1.append(flower.flowerSpecies.species)
		inventoryLabel.setText('Inventory: %s'%list1)
		print("type: "+str(flower1.flowerSpecies.species))
		print("age: "+str(flower1.age))
		print("ageRate: "+str(flower1.ageRate))
	else:
		print("no money left!")
	return

def createBouquet():
	pass

def foundShop():
	pass

random.seed()

money = 5

app = PyQt5.QtWidgets.QApplication(sys.argv)
ex = MainWindow(money)

app.exec()