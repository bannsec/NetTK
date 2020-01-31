#!/usr/bin/python

import sys
sys.path.append(".")

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from time import ctime
from database import getRows
from helpers import footer

def addTimeTicks(timeStamps, ax):
	# Verify there's actually timeStamps to work on
	if len(timeStamps) == 0:
		return

	# Add human readable times
	xticklabel = [ctime(timeStamps[0])]
	xticklabel.append(ctime(timeStamps[int(len(timeStamps)*0.2)]))
	xticklabel.append(ctime(timeStamps[int(len(timeStamps)*0.4)]))
	xticklabel.append(ctime(timeStamps[int(len(timeStamps)*0.6)]))
	xticklabel.append(ctime(timeStamps[int(len(timeStamps)*0.8)]))
	xticklabel.append(ctime(timeStamps[-1]))

	# Calculate where the ticks should be
	xtick = [timeStamps[0]]
	xtick.append(timeStamps[int(len(timeStamps)*0.2)])
	xtick.append(timeStamps[int(len(timeStamps)*0.4)])
	xtick.append(timeStamps[int(len(timeStamps)*0.6)])
	xtick.append(timeStamps[int(len(timeStamps)*0.8)])
	xtick.append(timeStamps[-1])

	# plt.xticks( xtick, xticklabel )
	ax.set_xticks(xtick)
	ax.set_xticklabels(xticklabel)

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

	# Create as many plots as we need to
	# TODO: Allow customization of view
	fig,ax = plt.subplots(nrows=len(plots), ncols=1, sharex=sharex, sharey=sharey)

	# Loop through our registered plots
	for plot in plots:

		# Grab our row information
		timeStamps, isDroppedPacket, delayTime = getRows(plot["table"], age=plot["age"])

		# Move over our ax element. If only one registered plot, this will be ax itself, it more than one, it will be in a numpy array.
		# Make sure we're looking at a list
		if isinstance(ax,np.ndarray) == True:
			# Numpy won't let us pop. We'll grab the top, then remove it.
			plot["ax"] = ax[0]
			ax = np.delete(ax,0, axis=0)
		else:
			# This is the case where we're only plotting one thing. Just copy it over.
			plot["ax"] = ax

		# Plot our initial data points, saving the line object we will use later to update it for animations.
		# TODO: Allow customization here
		plot["line"] = plot["ax"].plot(timeStamps, delayTime, '-', linewidth=1)[0]

		# Format the background grid
		#ax.grid(color='r', linestyle='--', linewidth=1)
		# TODO: Allow customization here
		plot["ax"].grid(True, 'major')

		# Set our axis labels.
		plot["ax"].set_xlabel("time (local time)")
		plot["ax"].set_ylabel("round trip time (s)")

		# Set plot title based on plot parameters
		plot["ax"].set_title(plot["title"])

		# Add human fiendly times along the bottom
		addTimeTicks(timeStamps, plot["ax"])

	# Add the footer
	footer(plt)

def dataGen():
	# TODO: Make this something useful... Just adding it now because it's required.
	while True:
		yield 1

def updateGraph(data):
	global line

	# Update all our plots
	for plot in plots:

		# Grab our row information
		timeStamps, isDroppedPackets, delayTimes = getRows(plot["table"], age=plot["age"])
	
		# Add new data to the graph
		plot["line"].set_data(timeStamps, delayTimes)

		# Auto fit the graph
		plot["ax"].relim()		# reset intern limits of the current axes
		plot["ax"].autoscale_view()	# reset axes limits 

		# Change x ticks to be human readable
		addTimeTicks(timeStamps, plot["ax"])

	# Draw the graph
	fig.canvas.draw()

	return None,


def lineGraphRun(**args):
	"""
	Input:
		Dictionary of arguments
	Action:
		Starts up graphs based off of input
	Returns:
		Nothing
	"""

	global plots, sharex, sharey

	# sharex, sharey boolen conversion
	sharex = args["sharex"].lower() in ["true", "yes", "1", "y"]
	sharey = args["sharex"].lower() in ["true", "yes", "1", "y"]

	# Parse out plots
	i = 1

	# Use this to loop thorugh the plots
	while ("alias_%s" % i) in args:
		
		# Append a new plot
		plots.append({
			"table"	: args["alias_%s" % i] + "_" + args["tag_%s" % i],
			"age"	: args["age_%s" % i],
			"title"	: args["title_%s" % i]

		})

		# Increment the counter
		i += 1

	# Create the initial graph
	buildGraph()

	# Register the animation
	# TODO: Currently live updating is very inefficient :(
	# TODO: Give option to animate or not
	im_ani = animation.FuncAnimation(fig, updateGraph, dataGen, interval=1000)

	# TODO: Give option to examine date range instead of age.

	# Start it up
	plt.show()	

	# Exit cleanly after
	exit(0)


# Programmatically define what we want to be looking at
plots = []
sharex = False
sharey = False

