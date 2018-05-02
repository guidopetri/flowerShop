#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#python 3.6.4

from enum import Enum

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
