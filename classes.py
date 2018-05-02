#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#python 3.6.4

from enum import Enum #so we can remain sane
import sys
import PyQt5.QtWidgets
import PyQt5.QtCore
import PyQt5.QtGui
import random #for randomization functions
import json #for saving our settings
import collections
import enums
import saving

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

class savedBouquet:
	def __init__(self,name,flowersDict,window):
		self.name = name
		self.flowers = flowersDict
		window.savedBouquetsList.append(self)

class BouquetInstance:
	def __init__(self,name,flowersDict):
		self.name = name
		self.flowers = flowersDict
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
		self.flowerSpeciesList = self.initFlowers()
		self.savedBouquetsList = []
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
		saveAct.triggered.connect(saving.saveGame)

		shopViewAct = PyQt5.QtWidgets.QAction(PyQt5.QtGui.QIcon('media/images/shopIcon.png'),'Shop',self)
		shopViewAct.triggered.connect(self.viewShops)

		overViewAct = PyQt5.QtWidgets.QAction(PyQt5.QtGui.QIcon('media/images/overviewIcon.png'),'Overview',self)
		overViewAct.triggered.connect(lambda:self.overView())

		bouquetCreateViewAct = PyQt5.QtWidgets.QAction(PyQt5.QtGui.QIcon('media/images/bouquetIcon.png'),'Bouquet',self)
		bouquetCreateViewAct.triggered.connect(self.createBouquetsView)

		bouquetViewAct = PyQt5.QtWidgets.QAction(PyQt5.QtGui.QIcon('media/images/bouquetIcon.png'),'Bouquet',self)
		bouquetViewAct.triggered.connect(self.viewBouquets)

		bouquetMenu = PyQt5.QtWidgets.QMenu(self)
		bouquetMenu.addAction(bouquetViewAct)
		bouquetMenu.addAction(bouquetCreateViewAct)

		flowerViewAct = PyQt5.QtWidgets.QAction(PyQt5.QtGui.QIcon('media/images/flowerIcon.png'),'Flower',self)
		flowerViewAct.triggered.connect(self.viewFlowers)

		#add actions to toolbars
		toolbarFunctions.addAction(exitAct)
		toolbarFunctions.addAction(saveAct)

		toolbarViews.addAction(overViewAct)
		toolbarViews.addAction(shopViewAct)
		#toolbarViews.addMenu(bouquetMenu)
		toolbarViews.addAction(bouquetViewAct)
		toolbarViews.addAction(bouquetCreateViewAct)
		toolbarViews.addAction(flowerViewAct)

		#main overview screen
		self.overView()

	def center(self):
		qr = self.frameGeometry()
		cp = PyQt5.QtWidgets.QDesktopWidget().availableGeometry().center()
		qr.moveCenter(cp)
		self.move(qr.topLeft())

	def initFlowers(self):
		Lotus = FlowerSpecies([enums.Color.RED],enums.Flowers.LOTUS,[enums.Sizes.MEDIUM,enums.Sizes.LARGE,enums.Sizes.LEGENDARY],10,[enums.Months.APR,enums.Months.MAY,enums.Months.JUN,enums.Months.JUL,enums.Months.AUG])
		Rose = FlowerSpecies([enums.Color.RED],enums.Flowers.ROSE,[enums.Sizes.MEDIUM,enums.Sizes.LARGE,enums.Sizes.LEGENDARY],10,[enums.Months.APR,enums.Months.MAY,enums.Months.JUN,enums.Months.JUL,enums.Months.AUG])
		Tulip = FlowerSpecies([enums.Color.RED],enums.Flowers.TULIP,[enums.Sizes.MEDIUM,enums.Sizes.LARGE,enums.Sizes.LEGENDARY],10,[enums.Months.APR,enums.Months.MAY,enums.Months.JUN,enums.Months.JUL,enums.Months.AUG])
		Sunflower = FlowerSpecies([enums.Color.RED],enums.Flowers.SUNFLOWER,[enums.Sizes.MEDIUM,enums.Sizes.LARGE,enums.Sizes.LEGENDARY],10,[enums.Months.APR,enums.Months.MAY,enums.Months.JUN,enums.Months.JUL,enums.Months.AUG])
		Daisy = FlowerSpecies([enums.Color.RED],enums.Flowers.DAISY,[enums.Sizes.MEDIUM,enums.Sizes.LARGE,enums.Sizes.LEGENDARY],10,[enums.Months.APR,enums.Months.MAY,enums.Months.JUN,enums.Months.JUL,enums.Months.AUG])
		Magnolia = FlowerSpecies([enums.Color.RED],enums.Flowers.MAGNOLIA,[enums.Sizes.MEDIUM,enums.Sizes.LARGE,enums.Sizes.LEGENDARY],10,[enums.Months.APR,enums.Months.MAY,enums.Months.JUN,enums.Months.JUL,enums.Months.AUG])
		Daffodil = FlowerSpecies([enums.Color.RED],enums.Flowers.DAFFODIL,[enums.Sizes.MEDIUM,enums.Sizes.LARGE,enums.Sizes.LEGENDARY],10,[enums.Months.APR,enums.Months.MAY,enums.Months.JUN,enums.Months.JUL,enums.Months.AUG])
		Iris = FlowerSpecies([enums.Color.RED],enums.Flowers.IRIS,[enums.Sizes.MEDIUM,enums.Sizes.LARGE,enums.Sizes.LEGENDARY],10,[enums.Months.APR,enums.Months.MAY,enums.Months.JUN,enums.Months.JUL,enums.Months.AUG])
		Carnation = FlowerSpecies([enums.Color.RED],enums.Flowers.CARNATION,[enums.Sizes.MEDIUM,enums.Sizes.LARGE,enums.Sizes.LEGENDARY],10,[enums.Months.APR,enums.Months.MAY,enums.Months.JUN,enums.Months.JUL,enums.Months.AUG])
		Jasmine = FlowerSpecies([enums.Color.RED],enums.Flowers.JASMINE,[enums.Sizes.MEDIUM,enums.Sizes.LARGE,enums.Sizes.LEGENDARY],10,[enums.Months.APR,enums.Months.MAY,enums.Months.JUN,enums.Months.JUL,enums.Months.AUG])
		Lily = FlowerSpecies([enums.Color.RED],enums.Flowers.LILY,[enums.Sizes.MEDIUM,enums.Sizes.LARGE,enums.Sizes.LEGENDARY],10,[enums.Months.APR,enums.Months.MAY,enums.Months.JUN,enums.Months.JUL,enums.Months.AUG])
		Cherry_Blossom = FlowerSpecies([enums.Color.RED],enums.Flowers.CHERRY_BLOSSOM,[enums.Sizes.MEDIUM,enums.Sizes.LARGE,enums.Sizes.LEGENDARY],10,[enums.Months.APR,enums.Months.MAY,enums.Months.JUN,enums.Months.JUL,enums.Months.AUG])
		Pansy = FlowerSpecies([enums.Color.RED],enums.Flowers.PANSY,[enums.Sizes.MEDIUM,enums.Sizes.LARGE,enums.Sizes.LEGENDARY],10,[enums.Months.APR,enums.Months.MAY,enums.Months.JUN,enums.Months.JUL,enums.Months.AUG])
		Violet = FlowerSpecies([enums.Color.RED],enums.Flowers.VIOLET,[enums.Sizes.MEDIUM,enums.Sizes.LARGE,enums.Sizes.LEGENDARY],10,[enums.Months.APR,enums.Months.MAY,enums.Months.JUN,enums.Months.JUL,enums.Months.AUG])
		Marigold = FlowerSpecies([enums.Color.RED],enums.Flowers.MARIGOLD,[enums.Sizes.MEDIUM,enums.Sizes.LARGE,enums.Sizes.LEGENDARY],10,[enums.Months.APR,enums.Months.MAY,enums.Months.JUN,enums.Months.JUL,enums.Months.AUG])
		Lilac = FlowerSpecies([enums.Color.RED],enums.Flowers.LILAC,[enums.Sizes.MEDIUM,enums.Sizes.LARGE,enums.Sizes.LEGENDARY],10,[enums.Months.APR,enums.Months.MAY,enums.Months.JUN,enums.Months.JUL,enums.Months.AUG])
		Poinsettia = FlowerSpecies([enums.Color.RED],enums.Flowers.POINSETTIA,[enums.Sizes.MEDIUM,enums.Sizes.LARGE,enums.Sizes.LEGENDARY],10,[enums.Months.APR,enums.Months.MAY,enums.Months.JUN,enums.Months.JUL,enums.Months.AUG])
		Chrysanthemum = FlowerSpecies([enums.Color.RED],enums.Flowers.CHRYSANTHEMUM,[enums.Sizes.MEDIUM,enums.Sizes.LARGE,enums.Sizes.LEGENDARY],10,[enums.Months.APR,enums.Months.MAY,enums.Months.JUN,enums.Months.JUL,enums.Months.AUG])
		Bleeding_Heart = FlowerSpecies([enums.Color.RED],enums.Flowers.BLEEDING_HEART,[enums.Sizes.MEDIUM,enums.Sizes.LARGE,enums.Sizes.LEGENDARY],10,[enums.Months.APR,enums.Months.MAY,enums.Months.JUN,enums.Months.JUL,enums.Months.AUG])
		Babys_Breath = FlowerSpecies([enums.Color.RED],enums.Flowers.BABYS_BREATH,[enums.Sizes.MEDIUM,enums.Sizes.LARGE,enums.Sizes.LEGENDARY],10,[enums.Months.APR,enums.Months.MAY,enums.Months.JUN,enums.Months.JUL,enums.Months.AUG])
		Poppy = FlowerSpecies([enums.Color.RED],enums.Flowers.POPPY,[enums.Sizes.MEDIUM,enums.Sizes.LARGE,enums.Sizes.LEGENDARY],10,[enums.Months.APR,enums.Months.MAY,enums.Months.JUN,enums.Months.JUL,enums.Months.AUG])
		Bluebell = FlowerSpecies([enums.Color.RED],enums.Flowers.BLUEBELL,[enums.Sizes.MEDIUM,enums.Sizes.LARGE,enums.Sizes.LEGENDARY],10,[enums.Months.APR,enums.Months.MAY,enums.Months.JUN,enums.Months.JUL,enums.Months.AUG])
		Camomile = FlowerSpecies([enums.Color.RED],enums.Flowers.CAMOMILE,[enums.Sizes.MEDIUM,enums.Sizes.LARGE,enums.Sizes.LEGENDARY],10,[enums.Months.APR,enums.Months.MAY,enums.Months.JUN,enums.Months.JUL,enums.Months.AUG])
		Zinnia = FlowerSpecies([enums.Color.RED],enums.Flowers.ZINNIA,[enums.Sizes.MEDIUM,enums.Sizes.LARGE,enums.Sizes.LEGENDARY],10,[enums.Months.APR,enums.Months.MAY,enums.Months.JUN,enums.Months.JUL,enums.Months.AUG])
		Cosmo = FlowerSpecies([enums.Color.RED],enums.Flowers.COSMO,[enums.Sizes.MEDIUM,enums.Sizes.LARGE,enums.Sizes.LEGENDARY],10,[enums.Months.APR,enums.Months.MAY,enums.Months.JUN,enums.Months.JUL,enums.Months.AUG])
		Jacobs_Ladder = FlowerSpecies([enums.Color.RED],enums.Flowers.JACOBS_LADDER,[enums.Sizes.MEDIUM,enums.Sizes.LARGE,enums.Sizes.LEGENDARY],10,[enums.Months.APR,enums.Months.MAY,enums.Months.JUN,enums.Months.JUL,enums.Months.AUG])
		Rafflesia = FlowerSpecies([enums.Color.RED],enums.Flowers.RAFFLESIA,[enums.Sizes.MEDIUM,enums.Sizes.LARGE,enums.Sizes.LEGENDARY],10,[enums.Months.APR,enums.Months.MAY,enums.Months.JUN,enums.Months.JUL,enums.Months.AUG])
		Passiflora = FlowerSpecies([enums.Color.RED],enums.Flowers.PASSIFLORA,[enums.Sizes.MEDIUM,enums.Sizes.LARGE,enums.Sizes.LEGENDARY],10,[enums.Months.APR,enums.Months.MAY,enums.Months.JUN,enums.Months.JUL,enums.Months.AUG])
		Dandelion = FlowerSpecies([enums.Color.RED],enums.Flowers.DANDELION,[enums.Sizes.MEDIUM,enums.Sizes.LARGE,enums.Sizes.LEGENDARY],10,[enums.Months.APR,enums.Months.MAY,enums.Months.JUN,enums.Months.JUL,enums.Months.AUG])
		Gayfeather = FlowerSpecies([enums.Color.RED],enums.Flowers.GAYFEATHER,[enums.Sizes.MEDIUM,enums.Sizes.LARGE,enums.Sizes.LEGENDARY],10,[enums.Months.APR,enums.Months.MAY,enums.Months.JUN,enums.Months.JUL,enums.Months.AUG])
		flowersList = [Lotus,Rose,Tulip,Sunflower,Daisy,Magnolia,Daffodil,Iris,Carnation,Jasmine,Lily,Cherry_Blossom,Pansy,Violet,Marigold,Lilac,Poinsettia,Chrysanthemum,Bleeding_Heart,Babys_Breath,Poppy,Bluebell,Camomile,Zinnia,Cosmo,Jacobs_Ladder,Rafflesia,Passiflora,Dandelion,Gayfeather]
		return flowersList

	def nextDay(self,account,moneyLabel,inventoryLabel):
		for shop in account.ShopCollection:
			for flower in shop.flowerStock:
				if random.randint(1,100) > 50:
					account.money+=flower.price
					shop.flowerStock.remove(flower)
				else:
					flower.senesce()
			moneyLabel.setText('Money: %s'%str(account.money))
			inventoryLabel.clear()
			for flower in account.ShopCollection[0].flowerStock:
				inventoryLabel.addItem(flower.flowerSpecies.species.name)
		return

	def viewShops(self):
		pass

	def viewBouquets(self):
		bouquetNameField = PyQt5.QtWidgets.QLineEdit()
		bouquetNameField.setReadOnly(True)
		inventoryBouquets = PyQt5.QtWidgets.QListWidget()
		for item in self.savedBouquetsList:
			inventoryBouquets.addItem(item.name)
		inventoryBouquetDetail = PyQt5.QtWidgets.QListWidget()
		inventoryBouquets.itemClicked.connect(lambda:self.viewBouquetDetails(bouquetNameField,inventoryBouquets.currentItem().text(),inventoryBouquetDetail))

		grid = PyQt5.QtWidgets.QGridLayout()
		grid.addWidget(bouquetNameField,1,1,1,2)
		grid.addWidget(inventoryBouquets,2,1)
		grid.addWidget(inventoryBouquetDetail,2,2)

		mainWidget = PyQt5.QtWidgets.QWidget(self)
		mainWidget.setLayout(grid)
		self.setCentralWidget(mainWidget)

		self.show()

		return

	def viewBouquetDetails(self,nameField,bouquetName,inventoryList):
		nameField.setText(bouquetName)
		for item in self.savedBouquetsList:
			if item.name == bouquetName:
				bouquet = item
		inventoryList.clear()
		for item,count in bouquet.flowers.items():
			for i in range(0,count):
				inventoryList.addItem(item)
		return

	def createBouquetsView(self):
		bouquetNameField = PyQt5.QtWidgets.QLineEdit('Bouquet Name')
		inventoryFlowers = PyQt5.QtWidgets.QListWidget()
		for item in self.flowerSpeciesList:
			inventoryFlowers.addItem(item.species.name)
		inventoryBouquet = PyQt5.QtWidgets.QListWidget()
		addFlowerButton = PyQt5.QtWidgets.QPushButton('Add Flower')
		addFlowerButton.clicked.connect(lambda:inventoryBouquet.addItem(inventoryFlowers.currentItem().text()))
		createBouquetButton = PyQt5.QtWidgets.QPushButton('Create Bouquet')
		createBouquetButton.clicked.connect(lambda:self.createBouquet(inventoryBouquet,bouquetNameField))

		grid = PyQt5.QtWidgets.QGridLayout()
		grid.addWidget(bouquetNameField,1,1,1,2)
		grid.addWidget(inventoryFlowers,2,1)
		grid.addWidget(inventoryBouquet,2,2)
		grid.addWidget(addFlowerButton,3,2)
		grid.addWidget(createBouquetButton,4,1,1,2)

		mainWidget = PyQt5.QtWidgets.QWidget(self)
		mainWidget.setLayout(grid)
		self.setCentralWidget(mainWidget)

		self.show()

		return

	def viewFlowers(self):
		pass

	def overView(self):
		Shop1 = Shop([],[],enums.Locations.SUBWAY,[],[],[],{})
		mainAccount = Account(5,[Shop1])
		#create buttons
		btn1 = PyQt5.QtWidgets.QPushButton('Next Day')
		btn1.clicked.connect(lambda:self.nextDay(mainAccount,moneyLabel,inventoryLabel))
		btn2 = PyQt5.QtWidgets.QPushButton('Quit')
		btn2.clicked.connect(PyQt5.QtWidgets.QApplication.instance().quit)
		moneyLabel = PyQt5.QtWidgets.QLabel('Money: %s'%str(mainAccount.money))
		list1 = []
		inventoryLabel = PyQt5.QtWidgets.QListWidget()
		for flower in mainAccount.ShopCollection[0].flowerStock:
			inventoryLabel.addItem(flower.flowerSpecies.species.name)
		#flowerCreateButton1 = PyQt5.QtWidgets.QPushButton('Buy Rose Flower')
		#flowerCreateButton1.clicked.connect(lambda:createFlower(window.flowerSpeciesList,Flowers.ROSE,moneyLabel))
		#flowerCreateButton2 = PyQt5.QtWidgets.QPushButton('Buy Tulip Flower')
		#flowerCreateButton2.clicked.connect(lambda:createFlower(window.flowerSpeciesList,Flowers.TULIP,moneyLabel))

		flowerCombo = PyQt5.QtWidgets.QComboBox(self)
		flowerCombo.addItems([str(item.species.name) for item in self.flowerSpeciesList])

		buyButton = PyQt5.QtWidgets.QPushButton('Buy')
		buyButton.clicked.connect(lambda:self.createFlower(self.flowerSpeciesList,flowerCombo.currentText(),mainAccount,moneyLabel,inventoryLabel))

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

		mainWidget = PyQt5.QtWidgets.QWidget(self)
		mainWidget.setLayout(grid)
		self.setCentralWidget(mainWidget)

		self.show()
		return

	def createFlower(self,flowerSpeciesList,flowerTypeStr,account,moneyLabel,inventoryLabel):
		for flower in enums.Flowers:
			if flower.name == flowerTypeStr:
				flowerType = flower
		if account.money >= 1:
			account.money -= 1
			moneyLabel.setText('Money: %s'%str(account.money))
			flower1 = Flower(2.5,enums.Color.RED,flowerSpeciesList[flowerType.value],enums.Sizes.MEDIUM,random.randint(1,5),random.randint(1,3))
			account.ShopCollection[0].flowerStock.append(flower1)
			inventoryLabel.addItem(flower1.flowerSpecies.species.name)
			print("type: "+str(flower1.flowerSpecies.species))
			print("age: "+str(flower1.age))
			print("ageRate: "+str(flower1.ageRate))
		else:
			print("no money left!")
		return

	def createBouquet(self,inventoryBouquet,nameField):
		bouquetFlowers = []
		for row in range(0,inventoryBouquet.count()):
			bouquetFlowers.append(inventoryBouquet.item(row).text())
		flowersDict = collections.Counter(bouquetFlowers)
		newBouquet = savedBouquet(nameField.text(),flowersDict,self)
		inventoryBouquet.clear()
		print("new bouquet %s created!"%nameField.text())

	def foundShop(self):
		pass