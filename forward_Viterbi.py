#!/home/bixichao/bin/python 
import sys
import os
import numpy as np
from Viterbi_data import generate_data
'''
	Parameter illustration:
			O:	the observation space 			n_observation*1
			S:	the state space 			n_state*1
			Y:	a sequence of obsercations 		n_seq_observation*1
			A:	transition matrix 			n_state*n_state
			B:	emission matrix 			n_state*n_observation
			PI:	an array of initial probabilities	n_state*1
	Input: sequence.fa
	Output: Px: the probabilities of observation x
'''
if __name__ == '__main__':
	if len(sys.argv) != 2:
		print 'usage wrong!!!'
		sys.exit(0)
	print sys.argv
	sequence_file = sys.argv[1]
	O,S,Y,A,B,PI,Y_state = generate_data(sequence_file)
#	print O#---right
#	print S#---right
#	print Y#---right
	n_state = len(S)
	n_seq_observation = len(Y)
	F = np.zeros((n_state,n_seq_observation+1))
	F[0][0] = 1
	for i in range(n_seq_observation+1):
		if i == 0:
			continue
		for l in range(n_state):
			for k in range(n_state):
				F[l][i] = F[l][i] + B[l][int(Y[i-1])-1]*F[k][i-1]*A[k][l]
	Px = 0
	for i in range(n_state):
		Px = Px + F[i][n_seq_observation]
	print Px#---right
################################################################################################
	count = 0#---right
	for i in range(n_state):#---right
		for j in range(n_seq_observation+1):#---right
			if F[i][j] != 0:#---right
				count = count + 1#---right
#				print F[i][j]#---right
	print '\n' + str(count)#---right
#	print '@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@'
#	for i in range(n_state):#---right
#		print F[i][0]	#---right
#	print '@@@@@@@@@@@@@@@@@@@@@@@@@@@'
#	for i in range(n_state):#---right
#		print F[i][1]#---right
#	print '@@@@@@@@@@@@@@@@@@@@@@@@@@@'
#	for i in range(n_state):#---right
#		print F[i][2]#---right
#	print '@@@@@@@@@@@@@@@@@@@@@@@@@@@'
#	for i in range(n_state):#---right
#		print F[i][n_seq_observation]#---right
