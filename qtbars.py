# qtbars version 1
# a program to graph progress

import sys
from PyQt5.QtWidgets import (QApplication,QDialog,
  QGridLayout, QLineEdit, QPushButton, QLabel,
	QFormLayout, QHBoxLayout, QVBoxLayout,
	QWidget)

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

import random
import numpy as np
import datetime

# Global constants
entriesNo = 5 # number of tasks
inputBoxes = [None] * entriesNo # NOT a numpy array - makes empty array of length 5

class Window(QDialog):

	def __init__(self, parent=None):
		super(Window, self).__init__(parent)
		self.setWindowTitle("qtbars (in development)")

		# a figure instance to plot on
		self.figure = Figure()

		# this is the Canvas Widget that displays the `figure`
		# it takes the `figure` instance as a parameter to __init__
		self.canvas = FigureCanvas(self.figure)

		# this is the Navigation widget
		# it takes the Canvas widget and a parent
		self.toolbar = NavigationToolbar(self.canvas, self)

		# Just some button connected to `plot` method
		self.button = QPushButton('Plot')
		self.button.clicked.connect(self.plot)

		# Another button to clear all numerical inputs
		self.button2 = QPushButton("Clear")
		self.button2.clicked.connect(self.clearNumbers)

		# set the layout
		beegLayout = QHBoxLayout()
		
		leftLayout = QVBoxLayout()
		leftLayout.addWidget(self.toolbar)
		leftLayout.addWidget(self.canvas)
		beegLayout.addLayout(leftLayout)

		rightLayout = QVBoxLayout()
		rightLayout.addWidget(QLabel("<h1>&nbsp;&nbsp; qtbars (v0)<\h1>"))
		# rightLayout.addWidget(QLabel("Enter current progress:"))

		courseLayout = QFormLayout()
		for i in range(entriesNo):
			inputBoxes[i] = QLineEdit()
			rowLabel = "Task " + str(i)
			courseLayout.addRow(rowLabel,inputBoxes[i])
		rightLayout.addLayout(courseLayout)

		rightLayout.addWidget(self.button)
		rightLayout.addWidget(self.button2)
		# "Plot" button is first, so pressing enter after inputting numbers will plot

		beegLayout.addLayout(rightLayout)
		
		self.setLayout(beegLayout)

	def randomplot(self): # plot random data (as gui test)
		data = [random.random() for i in range(10)]
		# Discards the old graph
		self.figure.clear()
		# Create an axis
		ax = self.figure.add_subplot(111)
		# try to change graph's background color?
		# ax.fill_between(facecolor=[0.94,0.94,0.94]) # hex is #efefef
		# Plot data
		ax.plot(data, '*-')
		# Refresh canvas
		self.canvas.draw()

	def evaluate(self,expression):
		try:
			# result = str(eval(expression, {}, {}))
			result = eval(expression, {}, {})
		except Exception:
			result = "Couldn't evaluate expression :(" 
			# does not catch a specific exception
		return result
		# relies on eval() which is a security risk

	def crunch(self): # go through inputs and evaluate them
		entries = [None] * entriesNo
		for i in range(entriesNo):
			entries[i] = self.evaluate(inputBoxes[i].text())
		return entries

	def plot(self):
		# self.randomplot() # plot random data as test

		self.figure.clear()
		ax = self.figure.add_subplot(111)
		# ax.fill_between(facecolor=[0.94,0.94,0.94]) # doesn't work yet
		entries = self.crunch()

		# assemble labels and data
		y_labels = [("Task " + str(i)) for i in range(entriesNo)]
		y_pos = np.arange(entriesNo)
		x_data = entries

		# make bar chart
		for i in range(entriesNo):
			if x_data[i] >= 0.80: # i.e. if done
				ax.barh(y_pos[i], x_data[i], color='tab:green')
			elif x_data[i] >= 0.75: # if mostly done
				ax.barh(y_pos[i], x_data[i], color='#006699')
			else:
				ax.barh(y_pos[i], x_data[i], color='orange')	
		
		# bar chart details
		# plt.gca().set_xlim([0, 1]) # optionally set graph limits? (broken)
		ax.set_yticks(y_pos, labels = y_labels)
		ax.invert_yaxis() # labels read top to bottom
		ax.set_xlabel('Progress')
		ax.set_title('Progress bars - {}'.format(datetime.datetime.now().strftime('%d %b')))

		self.canvas.draw()

	def clearNumbers(self):
		for i in range(entriesNo):
			inputBoxes[i].clear()

if __name__ == '__main__':
	app = QApplication(sys.argv)

	main = Window()
	main.show()

	sys.exit(app.exec_())
