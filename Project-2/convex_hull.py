from asyncio.windows_events import NULL
from pstats import SortKey
from types import NoneType
from which_pyqt import PYQT_VER
if PYQT_VER == 'PYQT5':
	from PyQt5.QtCore import QLineF, QPointF, QObject
elif PYQT_VER == 'PYQT4':
	from PyQt4.QtCore import QLineF, QPointF, QObject
else:
	raise Exception('Unsupported Version of PyQt: {}'.format(PYQT_VER))



import time

# Some global color constants that might be useful
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

RIGHT = 1
LEFT = -1
ZERO = 0

# Global variable that controls the speed of the recursion automation, in seconds
#
PAUSE = 0.25

# Simple bubble sort algorithm to sort the points by ther x values
def bubbleSort(points):
	n = len(points)
	for i in range(n - 1):
		for j in range(0, n - i - 1):
			if points[j].x() > points[j + 1].x():
				points[j], points[j + 1] = points[j + 1], points[j]	
	return points

def divide_hull(points):
	if len(points) == 1:
		return points

	left:list = divide_hull(points[0:len(points)//2])
	right:list = divide_hull(points[len(points)//2:len(points)])

	# Get a P and Q point for the max of the left and the min of the right
	P = max(left, key=lambda left: left.x())
	Q = min(right, key=lambda right: right.x())

	# Make copies of P and Q so that you have a set for the upper and lower lines
	P_copy, Q_copy = P, Q

	#for element in right:
	#	if direction(P, Q, element) == LEFT:
	#		Q = element

	P_prev, Q_prev = None, None
	while True:
		P_prev = P
		Q_prev = Q

		for q_next in right:
			if direction(P, Q, q_next) == LEFT:
				Q = q_next
				right.remove(Q_prev)
				Q_prev = Q
		
		for p_next in left:
			if direction(Q, P, p_next) == RIGHT:
				P = p_next
				left.remove(P_prev)
				P_prev = P
	
		if P == P_prev and Q == Q_prev:
			break

	PC_prev, QC_prev = None, None
	while True:
		PC_prev = P_copy
		QC_prev = Q_copy

		for q_next in right:
			if direction(P_copy, Q_copy, q_next) == RIGHT:
				Q_copy = q_next
				right.remove(QC_prev)
				QC_prev = Q_copy
		
		for p_next in left:
			if direction(Q_copy, P_copy, p_next) == LEFT:
				P_copy = p_next
				left.remove(PC_prev)
				PC_prev = P_copy
	
		if P_copy == PC_prev and Q_copy == QC_prev:
			break

	# Compare the tangent line angle from P to Q. If the angle increases
	# set Q to the next point that was increased. This should be done CLOCKWISE
	#for point in right:
	#	if point.y() > Q.y() and point.x() > Q.x():
	#		Q = point
	#		right.remove(Q)

	# Compare the tangent line angle from Q to P. If the angle increases
	# set P to the next point that was increased. This should be done COUNTER CLOCKWISE
	#for point in left:
	#	if point.y() > P.y() and point.x() > P.x():
	#		P = point
	#		left.remove(P)

	# Compare the tangent line angle from P to Q. If the angle decreases
	# set Q to the next point that was decreased. This should be COUNTER CLOCKWISE
	#for point in right:
	#	if point.y() < Q_copy.y() and point.x() < Q_copy.x():
	#		Q_copy = point
	#		right.remove(Q_copy)

	# Compare the tangent line angle from Q to P. If the angle decreases
	# set P to the next point that was decreased. This should be done CLOCKWISE
	#for point in left:
	#	if point.y() < P_copy.y() and point.x() < Q_copy.x():
	#		P_copy = point
	#		left.remove(P_copy)

	print("===Joining the new lists===")
	new_hull = left + right
	return new_hull

def direction(A, B, C):
	global RIGHT, LEFT, ZERO

	originX, originY = A.x(), A.y()
	BX, BY = B.x(), B.y()
	CX, CY = C.x(), C.y()

	BX -= originX
	BY -= originY
	CX -= originX
	CY -= originY

	cross_product = BX * CY - BY * CX

	if cross_product > 0:
		return RIGHT
	if cross_product < 0:
		return LEFT
	return ZERO


#
# This is the class you have to complete.
#
class ConvexHullSolver(QObject):

# Class constructor
	def __init__( self):
		super().__init__()
		self.pause = False
		
# Some helper methods that make calls to the GUI, allowing us to send updates
# to be displayed.

	def showTangent(self, line, color):
		self.view.addLines(line,color)
		if self.pause:
			time.sleep(PAUSE)

	def eraseTangent(self, line):
		self.view.clearLines(line)

	def blinkTangent(self,line,color):
		self.showTangent(line,color)
		self.eraseTangent(line)

	def showHull(self, polygon, color):
		self.view.addLines(polygon,color)
		if self.pause:
			time.sleep(PAUSE)
		
	def eraseHull(self,polygon):
		self.view.clearLines(polygon)
		
	def showText(self,text):
		self.view.displayStatusText(text)
	

# This is the method that gets called by the GUI and actually executes
# the finding of the hull
	def compute_hull( self, points, pause, view):
		self.pause = pause
		self.view = view
		assert( type(points) == list and type(points[0]) == QPointF )

		t1 = time.time()
		#cheater way to sort
		#points = sorted(points, key=lambda p: p.x())
		# bubble sort is n^2 time, so it needs to be changed to merge sort later
		points = bubbleSort(points)
		t2 = time.time()

		t3 = time.time()
		# this is a dummy polygon of the first 3 unsorted points
		points = divide_hull(points)
		polygon = [QLineF(points[i], points[(i+1)%len(points)]) for i in range(len(points))]
		# TODO: REPLACE THE LINE ABOVE WITH A CALL TO YOUR DIVIDE-AND-CONQUER CONVEX HULL SOLVER
		t4 = time.time()

		# when passing lines to the display, pass a list of QLineF objects.  Each QLineF
		# object can be created with two QPointF objects corresponding to the endpoints
		self.showHull(polygon,RED)
		self.showText('Time Elapsed (Convex Hull): {:3.3f} sec'.format(t4-t3))



