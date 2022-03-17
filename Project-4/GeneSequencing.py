#!/usr/bin/python3

from msilib import sequence
from which_pyqt import PYQT_VER
if PYQT_VER == 'PYQT5':
	from PyQt5.QtCore import QLineF, QPointF
elif PYQT_VER == 'PYQT4':
	from PyQt4.QtCore import QLineF, QPointF
else:
	raise Exception('Unsupported Version of PyQt: {}'.format(PYQT_VER))

import math
import time

# Used to compute the bandwidth for banded version
MAXINDELS = 3	# This is our d value

# Used to implement Needleman-Wunsch scoring
MATCH = -3
INDEL = 5	# Otherwise known as gap
SUB = 1		# Otherwise known as mismatch

class GeneSequencing:

	def __init__( self ):
		pass
	
# This is the method called by the GUI.  _sequences_ is a list of the ten sequences, _table_ is a
# handle to the GUI so it can be updated as you find results, _banded_ is a boolean that tells
# you whether you should compute a banded alignment or full alignment, and _align_length_ tells you 
# how many base pairs to use in computing the alignment
	def align(self, sequences, table, banded, align_length):
		self.banded = banded
		self.MaxCharactersToAlign = align_length
		results = []

		for i in range(len(sequences)):
			jresults = []
			for j in range(len(sequences)):

				if j < i:
					s = {}
				else:
###################################################################################################

					# Section of code implementation
					sequence_to_compute1 = sequences[i]
					sequence_to_compute1 = sequence_to_compute1[:self.MaxCharactersToAlign]

					sequence_to_compute2 = sequences[j]
					sequence_to_compute2 = sequence_to_compute2[:self.MaxCharactersToAlign]

					if banded:
						score, alignment1, alignment2 = self.banded_algorithm(sequence_to_compute1, sequence_to_compute2)
					else:
						score, alignment1, alignment2 = self.unrestricted_algorithm(sequence_to_compute1, sequence_to_compute2)

###################################################################################################
					s = {'align_cost':score, 'seqi_first100':alignment1, 'seqj_first100':alignment2}
					table.item(i,j).setText('{}'.format(int(score) if score != math.inf else score))
					table.update()
				jresults.append(s)
			results.append(jresults)
		return results

	# Unbanded algorithm implementation 
	def unrestricted_algorithm(self, seq1, seq2):
		n = len(seq1)
		m = len(seq2)
		score = self.init_matrix(m + 1, n + 1)

		# First fill out the first row and column. These will always
		# have the same value of indels * i or j
		for i in range(0, m + 1):
			score[i][0] = INDEL * i
		
		for i in range(0, n + 1):
			score[0][i] = INDEL * i
		
		# next calculate all the scores for all positions from (1,1) to (n,m)
		for i in range(1, m + 1):
			for j in range(1, n + 1):
				# We compare what the cheapest move will be by calculating a match,
				# deletion, or insertion, then choosing the minimum to be the current
				# cell's score. 
				match = score[i - 1][j - 1] + self.match_score(seq1[j - 1], seq2[i - 1])
				delete = score[i - 1][j] + INDEL
				insert = score[i][j - 1] + INDEL
				score[i][j] = min(match, delete, insert)

		# Create variables to hold alignments
		align1 = ""
		align2 = ""
		# Start at bottom right cell
		i = m
		j = n

		# Now begin backtracking by starting from the bottom right cell. Compute which
		# cell was taken in order to get to the current position then record that step
		# to each alignment string. Stop once you reach one of the edges of the matrix
		# or the origin
		while i > 0 and j > 0:
			score_current = score[i][j]
			score_diagonal = score[i - 1][j - 1]
			score_up = score[i][j - 1]
			score_left = score[i - 1][j]

			if score_current == score_diagonal + self.match_score(seq1[j - 1], seq2[i - 1]):
				align1 += seq1[j - 1]
				align2 += seq2[i - 1]
				i -= 1
				j -= 1
			elif score_current == score_up + INDEL:
				align1 += seq1[j - 1]
				align2 += '-'
				j -= 1
			elif score_current == score_left + INDEL:
				align1 += '-'
				align2 += seq2[i - 1]
				i -= 1
		
		# If i became 0 before j did, loop until j becomes 0 as well
		while j > 0:
			align1 += seq1[j - 1]
			align2 += '-'
			j -= 1
		
		# If j became 0 before i did, loop until i becomes 0 as well
		while i > 0:
			align1 += '-'
			align2 += seq2[i - 1]
			i -= 1
		
		# flip the alignment paths
		align1 = align1[::-1]
		align2 = align2[::-1]

		# score[m][n] will be the final score in the bottom right corner
		return(score[m][n], align1, align2)

	# Banded Algorithm implementation
	def banded_algorithm(self, seq1, seq2):
		# Just tests to see if we are trying to align sequences that are too different in length
		# Notice that the cutoff is a difference of 50, so if each sequence was only 20 characters
		# long, it would not be stopped from aligning the test sequences with the genetic sequences
		if len(seq1) - len(seq2) > 50 or len(seq2) - len(seq1) > 50:
			return(math.inf, "No Alignment Possible", "No Alignment Possible")
		
		n = len(seq1)
		m = len(seq2)
		score = self.init_matrix(m + 1, n + 1)
		final_score = 0

		for i in range(0, 4):
			score[i][0] = INDEL * i
		
		for i in range(0, 4):
			score[0][i] = INDEL * i

		for i in range(1, m + 1):
			for j in range(1, n + 1):
				# This is pretty much the same as before, but now we disregard calculating
				# scores that are too far away from the diagonal center in the band
				if j - i <= MAXINDELS and i - j <= MAXINDELS:
					match = score[i - 1][j - 1] + self.match_score(seq1[j - 1], seq2[i - 1])
					delete = score[i - 1][j] + INDEL
					insert = score[i][j - 1] + INDEL
					score[i][j] = min(match, delete, insert)
					final_score = score[i][j]

		# Create variables to hold alignments
		align1 = ""
		align2 = ""
		# Start at bottom right cell
		i = m
		j = n

		# Backtrack through the matrix in order to create the strings for each sequence
		while i > 0 and j > 0:
			score_current = score[i][j]
			score_diagonal = score[i - 1][j - 1]
			score_up = score[i][j - 1]
			score_left = score[i - 1][j]

			if score_current == score_diagonal + self.match_score(seq1[j - 1], seq2[i - 1]):
				align1 += seq1[j - 1]
				align2 += seq2[i - 1]
				i -= 1
				j -= 1
			elif score_current == score_up + INDEL:
				align1 += seq1[j - 1]
				align2 += '-'
				j -= 1
			elif score_current == score_left + INDEL:
				align1 += '-'
				align2 += seq2[i - 1]
				i -= 1

		# If i became 0 before j did, loop until it's 0
		while j > 0:
			align1 += seq1[j - 1]
			align2 += '-'
			j -= 1
		
		# If j became 0 before i did, loop until it's 0
		while i > 0:
			align1 += '-'
			align2 += seq2[i - 1]
			i -= 1
		
		# flip the alignment paths
		align1 = align1[::-1]
		align2 = align2[::-1]

		return(final_score, align1, align2)

	# Utility function for checking two separate points in the matrix and determining
	# their score for each other's relation
	def match_score(self, a, b):
		if a == b:
			return MATCH
		elif a == '-' or b == '-':
			return INDEL
		else:
			return SUB
	
	# This is a utility function that prints out the matrix to make sure
	# that the sequences are being computed correctly
	def print_matrix(self, mat):
		# Loop over all rows
		for i in range(0, len(mat)):
			print("[", end = "")
			# Loop over each column in row i
			for j in range(0, len(mat[i])):
				# Print out the value in row i, column j
				print(mat[i][j], end = "")
				# Only add a tab if we're not in the last column
				if j != len(mat[i]) - 1:
					print("\t", end = "")
			print("]\n")
	
	# Utility function that initializes the matrix with all 0's
	# The matrix dimensions will be of size n by m
	def init_matrix(self, rows, cols):
		matrix = []
		for x in range(rows):
			matrix.append([])
			for y in range(cols):
				matrix[-1].append(0)
		return matrix
	
	def init_banded_matrix(self, indels, seq1, seq2):
		matrix = []
		longest = 0
		if seq1 > seq2: 
			longest = seq1
		else:
			longest = seq2
		for x in range(longest):
			matrix.append([])
			for y in range((indels * 2) + 1):
				matrix[-1].append(0)
		return matrix


