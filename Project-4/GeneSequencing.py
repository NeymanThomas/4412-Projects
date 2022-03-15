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
MAXINDELS = 3

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
						return
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
		score = self.zeros(m + 1, n + 1)
		final_score = 0

		# First fill out the first row and column
		for i in range(0, m + 1):
			score[i][0] = INDEL * i
		
		for i in range(0, n + 1):
			score[0][i] = INDEL * i
		
		for i in range(1, m+1):
			for j in range(1, n + 1):
				# Calculate the scores
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
		
		while j > 0:
			align1 += seq1[j - 1]
			align2 += '-'
			j -= 1
		
		while i > 0:
			align1 += '-'
			align2 += seq2[i - 1]
			i -= 1
		
		# flip the alignment paths
		align1 = align1[::-1]
		align2 = align2[::-1]

		return(final_score, align1, align2)

	def banded_algorithm(self, seq1, seq2):
		return
	
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
	def zeros(self, rows, cols):
		retval = []
		for x in range(rows):
			retval.append([])
			for y in range(cols):
				retval[-1].append(0)
		return retval


