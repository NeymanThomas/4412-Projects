#!/usr/bin/python3

from typing import final
from which_pyqt import PYQT_VER
if PYQT_VER == 'PYQT5':
	from PyQt5.QtCore import QLineF, QPointF
elif PYQT_VER == 'PYQT4':
	from PyQt4.QtCore import QLineF, QPointF
else:
	raise Exception('Unsupported Version of PyQt: {}'.format(PYQT_VER))




import time
import numpy as np
import math
from TSPClasses import *
import heapq
import itertools



class TSPSolver:
	def __init__( self, gui_view ):
		self._scenario = None

	def setupWithScenario( self, scenario ):
		self._scenario = scenario


	''' <summary>
		This is the entry point for the default solver
		which just finds a valid random tour.  Note this could be used to find your
		initial BSSF.
		</summary>
		<returns>
		results dictionary for GUI that contains three ints: cost of solution, 
		time spent to find solution, number of permutations tried during search, the 
		solution found, and three null values for fields not used for this 
		algorithm
		</returns> 
	'''
	
	def defaultRandomTour( self, time_allowance=60.0 ):
		results = {}
		cities = self._scenario.getCities()
		ncities = len(cities)
		foundTour = False
		count = 0
		bssf = None
		start_time = time.time()
		while not foundTour and time.time()-start_time < time_allowance:
			# create a random permutation
			perm = np.random.permutation( ncities )
			route = []
			# Now build the route using the random permutation
			for i in range( ncities ):
				route.append( cities[ perm[i] ] )
			bssf = TSPSolution(route)
			count += 1
			if bssf.cost < np.inf:
				# Found a valid route
				foundTour = True
		end_time = time.time()
		results['cost'] = bssf.cost if foundTour else math.inf
		results['time'] = end_time - start_time
		results['count'] = count
		results['soln'] = bssf
		results['max'] = None
		results['total'] = None
		results['pruned'] = None
		return results


	''' <summary>
		This is the entry point for the branch-and-bound algorithm that you will implement
		</summary>
		<returns>results dictionary for GUI that contains three ints: cost of best solution, 
		time spent to find best solution, total number solutions found during search (does
		not include the initial BSSF), the best solution found, and three more ints: 
		max queue size, total number of states created, and number of pruned states.</returns> 
	'''

	def branchAndBound( self, time_allowance=60.0 ):
		# global variables to keep track of how the code is running
		global N
		global visited_cities
		global final_path
		global maxsize
		global final_result
		global count
		global cities
		global pruned
		global total_states
		global max_queue

		# init values
		cities = self._scenario.getCities()
		N = len(cities)
		final_path = [None] * (N + 1)
		visited_cities = [False] * N
		maxsize = np.inf
		final_result = maxsize
		pruned, total_states, count, max_queue = 0, 0, 0, 0

		# create a matrix that contains the distances to every city
		adjacency_matrix = []
		for i in range(N):
			temp = []
			for j in range(N):
				temp.append(cities[j].costTo(cities[i]))
				if j == N - 1:
					adjacency_matrix.append(temp)

		start_time = time.time()
		TSPSolver.BeginSearch(adjacency_matrix)
		end_time = time.time()
		
		# convert the list of vertexes to list of cities
		route = []
		for i in final_path:
			route.append(cities[i])
		route = route[:-1]
		
		# pass the route into the TSPSolution class
		bssf = TSPSolution(route)
		
		results = {}
		results['cost'] = bssf.cost
		results['time'] = end_time - start_time
		results['count'] = count
		results['soln'] = bssf
		results['max'] = max_queue
		results['total'] = total_states
		results['pruned'] = pruned
		return results


	# Function to find the minimum edge cost having an end at the vertex i
	def getFirstCost(adjacency_matrix, i):
		min = maxsize
		for k in range(N):
			if adjacency_matrix[i][k] < min and i != k:
				min = adjacency_matrix[i][k]
		return min

	# function to find the second minimum edge cost having an end at the vertex i
	def getSecondCost(adjacency_matrix, i):
		first, second = maxsize, maxsize
		for j in range(N):
			if i == j:
				continue
			if adjacency_matrix[i][j] <= first:
				second = first
				first = adjacency_matrix[i][j]
	
			elif(adjacency_matrix[i][j] <= second and 
				adjacency_matrix[i][j] != first):
				second = adjacency_matrix[i][j]
		return second
	
	# function computes initial bound using 1/2 * (sum of first min + second min) for all edges
	def initBound(adjacency_matrix):
		result = 0
		for i in range(N):
			a = maxsize
			for k in range(N):
				if adjacency_matrix[i][k] < a and i != k:
					a = adjacency_matrix[i][k]

			b, c = maxsize, maxsize
			for j in range(N):
				if i == j:
					continue
				if adjacency_matrix[i][j] <= b:
					c = b
					b = adjacency_matrix[i][j]
		
				elif(adjacency_matrix[i][j] <= c and 
					adjacency_matrix[i][j] != b):
					c = adjacency_matrix[i][j]
			result += a + c
		return result

	# function initializes the lower bound then begins the recursive search
	def BeginSearch(adjacency_matrix):
		# initialize the current_path
		current_path = [-1] * (N + 1)
	
		# create the initial bound
		current_bound = TSPSolver.initBound(adjacency_matrix)
		# Rounding off the lower bound to an integer
		current_bound = math.ceil(current_bound / 2)
	
		# Set the first values for the current path and visited cities
		visited_cities[0] = True
		current_path[0] = 0
	
		# Call to TSPRec for current_weight equal to 0 and level 1
		TSPSolver.RecursiveBranch(adjacency_matrix, current_bound, 0, 1, current_path, visited_cities)

	# current_bound is the lower bound of the root node
	# current_weight stores the weight of the path so far
	# level is the current level while moving in the search space tree
	# current_path[] is where the solution is being stored
	def RecursiveBranch(adjacency_matrix, current_bound, current_weight, level, current_path, visited_cities):
		global final_result
		global pruned
		global total_states
		global count
		global max_queue

		# base case
		# Once all levels have been reached we are done
		if level == N:
			# check if there is an edge from last city in path back to the first city
			if adjacency_matrix[current_path[level - 1]][current_path[0]] != 0 and adjacency_matrix[current_path[level - 1]][current_path[0]] != maxsize:
				# current_result has the total weight of the solution
				current_result = current_weight + adjacency_matrix[current_path[level - 1]][current_path[0]]
				if current_result < final_result:
					final_path[:N + 1] = current_path[:]
					final_path[N] = current_path[0]
					final_result = current_result
					count += 1
			return
	
		# iterate through all cities to build the search space tree
		for i in range(N):
			total_states += 1
			# Consider next city if it is not the same (diagonal entry in adjacency matrix and not visited_cities already)
			if (adjacency_matrix[current_path[level-1]][i] != maxsize and visited_cities[i] == False):
				temp = current_bound
				current_weight += adjacency_matrix[current_path[level - 1]][i]
	
				if level == 1:
					current_bound -= ((TSPSolver.getFirstCost(adjacency_matrix, current_path[level - 1]) + TSPSolver.getFirstCost(adjacency_matrix, i)) / 2)
				else:
					current_bound -= ((TSPSolver.getSecondCost(adjacency_matrix, current_path[level - 1]) + TSPSolver.getFirstCost(adjacency_matrix, i)) / 2)
	
				# current_bound + current_weight is the actual lower bound for the node that we have arrived on.
				# If current lower bound < final_result, then explore the node further
				if current_bound + current_weight < final_result:
					max_queue += 1
					current_path[level] = i
					visited_cities[i] = True
					TSPSolver.RecursiveBranch(adjacency_matrix, current_bound, current_weight, level + 1, current_path, visited_cities)
	
				# prune the node by resetting all changes to current_weight and current_bound
				current_weight -= adjacency_matrix[current_path[level - 1]][i]
				current_bound = temp
				pruned += 1
	
				# reset the visited_cities array
				visited_cities = [False] * len(visited_cities)
				for j in range(level):
					if current_path[j] != -1:
						visited_cities[current_path[j]] = True








	''' <summary>
		This is the entry point for the greedy solver, which you must implement for 
		the group project (but it is probably a good idea to just do it for the branch-and
		bound project as a way to get your feet wet).  Note this could be used to find your
		initial BSSF.
		</summary>
		<returns>results dictionary for GUI that contains three ints: cost of best solution, 
		time spent to find best solution, total number of solutions found, the best
		solution found, and three null values for fields not used for this 
		algorithm</returns> 
	'''

	def greedy( self,time_allowance=60.0 ):
		pass



	''' <summary>
		This is the entry point for the algorithm you'll write for your group project.
		</summary>
		<returns>results dictionary for GUI that contains three ints: cost of best solution, 
		time spent to find best solution, total number of solutions found during search, the 
		best solution found.  You may use the other three field however you like.
		algorithm</returns> 
	'''
		
	def fancy( self,time_allowance=60.0 ):
		pass
		



