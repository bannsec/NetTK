#
# Library of generally helpful things
#

from nettk.version import VERSION

def footer(plt):
	"""
	Input:
		plt = plt variable for plot we're writing on
	Action:
		Write NetTK footer on to plot that was input
	Returns:
		Nothing
	"""

	plt.figtext(0.02,0.02,"Powered By NetTK v{0} -- https://github.com/bannsec/NetTK".format(VERSION))
