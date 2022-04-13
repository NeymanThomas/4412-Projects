#!/usr/bin/python3

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
		global N
		global visited
		global final_path
		global maxsize
		global final_res

		cities = self._scenario.getCities()
		N = len(cities)
		final_path = [None] * (N + 1)
		visited = [False] * N
		maxsize = float('inf')
		final_res = maxsize

		adjacency_matrix = []
		for i in range(N):
			temp = []
			for j in range(N):
				temp.append(cities[j].costTo(cities[i]))
				if j == N - 1:
					adjacency_matrix.append(temp)

		start_time = time.time()
		TSPSolver.TSP(adjacency_matrix)
		end_time = time.time()

		#print("Minimum Cost: ", final_res)
		#print("Path Taken : ", end = ' ')
		#for i in range(N + 1):
		#	print(final_path[i], end = ' ')
		
		# convert the list of vertexes to list of cities
		route = []
		for i in final_path:
			route.append(cities[i])
		route = route[:-1]
		
		bssf = TSPSolution(route)
		for i in route:
			print(i._index)
		
		results = {}
		results['cost'] = bssf.cost
		results['time'] = end_time - start_time
		results['count'] = 69
		results['soln'] = bssf
		results['max'] = None
		results['total'] = None
		results['pruned'] = None
		return results

	# Function to copy temporary solution
	# to the final solution
	def copyToFinal(curr_path):
		final_path[:N + 1] = curr_path[:]
		final_path[N] = curr_path[0]

	# Function to find the minimum edge cost 
	# having an end at the vertex i
	def firstMin(adj, i):
		min = maxsize
		for k in range(N):
			if adj[i][k] < min and i != k:
				min = adj[i][k]
	
		return min

	# function to find the second minimum edge 
	# cost having an end at the vertex i
	def secondMin(adj, i):
		first, second = maxsize, maxsize
		for j in range(N):
			if i == j:
				continue
			if adj[i][j] <= first:
				second = first
				first = adj[i][j]
	
			elif(adj[i][j] <= second and 
				adj[i][j] != first):
				second = adj[i][j]
	
		return second

	# This function sets up final_path
	def TSP(adj):
		
		# Calculate initial lower bound for the root node 
		# using the formula 1/2 * (sum of first min + 
		# second min) for all edges. Also initialize the 
		# curr_path and visited array
		curr_bound = 0
		curr_path = [-1] * (N + 1)
		visited = [False] * N
	
		# Compute initial bound
		for i in range(N):
			curr_bound += (TSPSolver.firstMin(adj, i) + TSPSolver.secondMin(adj, i))
	
		# Rounding off the lower bound to an integer
		curr_bound = math.ceil(curr_bound / 2)
	
		# We start at vertex 1 so the first vertex 
		# in curr_path[] is 0
		visited[0] = True
		curr_path[0] = 0
	
		# Call to TSPRec for curr_weight 
		# equal to 0 and level 1
		TSPSolver.TSPRec(adj, curr_bound, 0, 1, curr_path, visited)

	# function that takes as arguments:
	# curr_bound -> lower bound of the root node
	# curr_weight-> stores the weight of the path so far
	# level-> current level while moving
	# in the search space tree
	# curr_path[] -> where the solution is being stored
	# which would later be copied to final_path[]
	def TSPRec(adj, curr_bound, curr_weight, level, curr_path, visited):
		global final_res

		# base case is when we have reached level N 
		# which means we have covered all the nodes once
		if level == N:
			
			# check if there is an edge from
			# last vertex in path back to the first vertex
			if adj[curr_path[level - 1]][curr_path[0]] != 0:
				
				# curr_res has the total weight
				# of the solution we got
				curr_res = curr_weight + adj[curr_path[level - 1]][curr_path[0]]

				if curr_res < final_res:
					TSPSolver.copyToFinal(curr_path)
					final_res = curr_res
			return
	
		# for any other level iterate for all vertices
		# to build the search space tree recursively
		for i in range(N):
			
			# Consider next vertex if it is not same 
			# (diagonal entry in adjacency matrix and 
			#  not visited already)
			if (adj[curr_path[level-1]][i] != 0 and
								visited[i] == False):
				temp = curr_bound
				curr_weight += adj[curr_path[level - 1]][i]
	
				# different computation of curr_bound 
				# for level 2 from the other levels
				if level == 1:
					curr_bound -= ((TSPSolver.firstMin(adj, curr_path[level - 1]) + TSPSolver.firstMin(adj, i)) / 2)
				else:
					curr_bound -= ((TSPSolver.secondMin(adj, curr_path[level - 1]) + TSPSolver.firstMin(adj, i)) / 2)
	
				# curr_bound + curr_weight is the actual lower bound 
				# for the node that we have arrived on.
				# If current lower bound < final_res, 
				# we need to explore the node further
				if curr_bound + curr_weight < final_res:
					curr_path[level] = i
					visited[i] = True
					
					# call TSPRec for the next level
					TSPSolver.TSPRec(adj, curr_bound, curr_weight, 
						level + 1, curr_path, visited)
	
				# Else we have to prune the node by resetting 
				# all changes to curr_weight and curr_bound
				curr_weight -= adj[curr_path[level - 1]][i]
				curr_bound = temp
	
				# Also reset the visited array
				visited = [False] * len(visited)
				for j in range(level):
					if curr_path[j] != -1:
						visited[curr_path[j]] = True












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
		



