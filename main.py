#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#python 3.6.4

#Flower Shop Ordering To Go - Create a flower shop application which deals in flower objects and use those flower objects in a bouquet object which can then be sold. Keep track of the number of objects and when you may need to order more.

import sys
import PyQt5.QtWidgets
import random #for randomization functions
import classes

random.seed()

money = 5.0

app = PyQt5.QtWidgets.QApplication(sys.argv)
ex = classes.MainWindow(money)

app.exec()