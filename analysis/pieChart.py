#!/usr/bin/env python3

import sys
sys.path.append(".")

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from time import ctime
from database import getRows
from helpers import footer


def buildGraph():
	"""
	Input:
		Nothing
	Action:
		Loops through all registered plots.
		Creates and initializes their graph.
		Updates plots global list.
	Returns:
		Nothing
	"""
	global line, fig, plots

	# Initialize ax (subplot holder)
	ax = None

	# Generate our figure object
	fig = plt.figure()

	# Loop through our registered plots
	for plot in plots:

		# Create the pie chart plot for this pie chart
		plot["ax"] = plt.subplot2grid((gridx,gridy), (plot["locy"],plot["locx"]), aspect=1)

		# Grab our row information
		timeStamps, isDroppedPacket, delayTime = getRows(plot["table"], age=plot["age"])

		# Plot our initial data points, saving the line object we will use later to update it for animations.
		# TODO: Allow customization here
		plot["ax"].pie([isDroppedPacket.count(0),isDroppedPacket.count(1)],[0,0.05],["Not Dropped","Dropped"], shadow=True, autopct="%.0f%%", startangle=45, colors=[colorGood,colorBad])

		# Set plot title based on plot parameters
		plot["ax"].set_title(plot["title"])

	# Add the footer
	footer(plt)

def dataGen():
	# TODO: Make this something useful... Just adding it now because it's required.
	while True:
		yield 1

def updateGraph(data):

	# Update all our plots
	for plot in plots:

		# Grab our row information
		timeStamps, isDroppedPackets, delayTimes = getRows(plot["table"], age=plot["age"])

		# Clear image. If we don't, it gets smudgy
		plot["ax"].clear()

		# Re-set the title
		plot["ax"].set_title(plot["title"])

		# Re-draw the chart
		plot["ax"].pie([isDroppedPackets.count(0),isDroppedPackets.count(1)],[0,0.05],["Not Dropped","Dropped"], shadow=True, autopct="%.0f%%", startangle=45, colors=[colorGood,colorBad])

		plot["ax"].relim()		# reset intern limits of the current axes
		plot["ax"].autoscale_view()	# reset axes limits 

	# Draw our pie charts
	fig.canvas.draw()

	return None,


def pieChartRun(**args):
	"""
	Input:
		Dictionary of arguments
	Action:
		Starts up graphs based off of input
	Returns:
		Nothing
	"""

	global plots, gridx, gridy, colorGood, colorBad

	# Parse out plots
	i = 1

	# Set our grid variables
	gridx = int(args["gridx"])
	gridy = int(args["gridy"])

	# Set our color variables
	if "colorgood" in args:
		colorGood = args["colorgood"]
	if "colorbad" in args:
		colorBad = args["colorbad"]

	# Use this to loop thorugh the plots
	while ("alias_%s" % i) in args:
		
		# Append a new plot
		plots.append({

			"table"	: args["alias_%s" % i] + "_" + args["tag_%s" % i],
			"age"	: args["age_%s" % i],
			"title"	: args["title_%s" % i],
			"locx" : int(args["locx_%s" % i]),
			"locy" : int(args["locy_%s" % i])

		})

		# Increment the counter
		i += 1

	# Create the initial graph
	buildGraph()

	# Register the animation
	# TODO: Currently live updating is very inefficient :(
	# TODO: Give option to animate or not
	im_ani = animation.FuncAnimation(fig, updateGraph, dataGen, interval=2000)

	# TODO: Give option to examine date range instead of age.

	# Start it up
	plt.show()	

	# Exit cleanly after
	exit(0)


# Programmatically define what we want to be looking at
plots = []

# Default colors
colorGood = "#7E8F7C"
colorBad = "#C63D0F"

