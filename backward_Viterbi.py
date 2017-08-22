#!/home/bixichao/bin/python 
from __future__ import division
import sys
import os 
import numpy as np
from Viterbi_data import generate_data

'''
	Parameter illustration:
		O:	the observation space			n_observation*1
		S:	the state space				n_state*1
		Y:	a sequence of obsercations		n_seq_observation*1
		A:	transition matrix			n_state*n_state
		B:	emission matrix				n_state*n_observation
		PI:	an array of initial probabilities	n_state*1
	Input:sequence.fa
	Output:
'''
if __name__ == '__main__':
	if len(sys.argv) != 2:
		print 'usage wrong!!!'
		sys.exit(0)
	print sys.argv
	sequence_file = sys.argv[1]
	O,S,Y,A,B,PI,Y_state = generate_data(sequence_file)
	n_state = len(S)
	n_seq_observation = len(Y)
########################################################
#forward algorithm
########################################################
	F = np.zeros((n_state,n_seq_observation+1),dtype = 'float64')
	F[0][0] = 1
	for i in range(n_seq_observation+1):
		if i == 0:
			continue
		for l in range(n_state):
			for k in range(n_state):
				F[l][i] = F[l][i] + B[l][int(Y[i-1])-1]*F[k][i-1]*A[k][l]
	Px1 = 0
	for i in range(n_state):
		Px1 = Px1 + F[i][n_seq_observation]
##########################################################
#backward algorithm
##########################################################
	b = np.zeros((n_state,n_seq_observation))
	for k in range(n_state):
		b[k][n_seq_observation-1] = A[k][0]
	for i in range(n_seq_observation)[::-1]:
		for k in range(n_state):
			for l in range(n_state):
				if i != (n_seq_observation-1):
					b[k][i] = b[k][i] + A[k][l]*B[l][int(Y[i+1])-1]*b[l][i+1]
#	for i in range(n_state):#---right
#		print b[i][n_seq_observation-1]#---right
#	for i in range(n_state):#---right
#		print b[i][n_seq_observation-2]#-right
	Px2 = 0
	for l in range(n_state):#---right
		print b[l][2]
		Px2 = Px2 + A[0][l]*B[l][int(Y[0])-1]*b[l][0]
	print '@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@'
	print Px1#---right
	print Px2#---right
	P = np.zeros((n_seq_observation,n_state),dtype = 'float64')
	for i in range(n_seq_observation):
		for j in range(n_state):
			P[i][j] = F[j][i+1]*(b[j][i]/Px1)
#	print '#############################'
#	for i in range(n_state):
#		print P[5][i]
#	print '########################'
#	for i in range(n_state):
#		print F[i][16]
#	print '##########################'
#	print Px1
#	print '#########################'
#	for i in range(n_state):
#		print b[i][16]
#	print '###########################'
#	test = (3.57113937447e-14*7.8930307721e-213)/3.5714925577e-225
#	print test
###############################################################################
#for testing
###############################################################################
#########
#example1
#########
#	pX = []
#	for i in range(n_seq_observation):
#		qq = [P[i][1],P[i][2],P[i][3],P[i][4],P[i][5],P[i][6]]
#		pX.append(max(qq))
#	g = open('result_plot','w')
#	count = 0
#	for i in range(n_seq_observation):
#		count = count + 1
#		g.write(str(count)+'\t'+str(pX[i])+'\n')
#	g.close()
#	print pX
#######
#R_plot
#######
#	os.system("Rscript plot_backward_Viterbi.R")
#########
#example2
#########
#	pX = []
#	index_x = []
#	for i in range(n_seq_observation):
#		qq = []
#		for j in range(n_state):
#			qq.append(P[i][j])
#		pX.append(max(qq))
#		index_x.append(qq.index(max(qq)))
#	print index_x
