#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#python 3.6.4

#Flower Shop Ordering To Go - Create a flower shop application which deals in flower objects and use those flower objects in a bouquet object which can then be sold. Keep track of the number of objects and when you may need to order more.

from enum import Enum
import PyQt5

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
		self.age = min([flower.age for flower in self.flowers.keys()])
		self.alive = True

	def senesce(self):
		for flower in self.flowers.keys():
			flower.senesce()
			if flower.alive == False:
				self.alive = False
		self.age = min([flower.age for flower in self.flowers.keys()])

class Shop:
	def __init__(self,flowerStock,stockPrices,flowerPrices,openingHours,employeesDict):
		self.flowerStock = flowerStock
		self.stockPrices = stockPrices
		self.flowerPrices = flowerPrices
		self.openingHours = openingHours
		self.employeesDict = employeesDict

class flowerOrder:
	def __init__(self,bouquetDict,totalPrice,deliveryDate,):
		self.bouquetDict = bouquetDict
		self.totalPrice = 0
		for bouquet,count in self.bouquetDict.items():
			self.totalPrice += count*bouquet.price

#testing
Rose = FlowerSpecies([Color.RED],Flowers.ROSE,[Sizes.TINY,Sizes.LEGENDARY],16,Months.DEC)
Daisy = FlowerSpecies([Color.GREEN],Flowers.DAISY,[Sizes.TINY],22,Months.DEC)
Flower1 = Flower(1,Color.RED,Rose,Sizes.LEGENDARY,15,1)
Flower2 = Flower(1,Color.GREEN,Daisy,Sizes.TINY,20,1)
dictFlowers = {Flower1:3,Flower2:2}
bouquet1 = Bouquet(dictFlowers)
print(bouquet1.age)
bouquet1.senesce()
print(bouquet1.age)
print(bouquet1.alive)