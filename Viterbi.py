#!/home/bixichao/bin/python 
from Viterbi_data import generate_data
import sys
import os
import numpy as np
'''
	Input:
		sequence.fa: the sequence you want to anlysis
	Output:
		result.txt
	PS: this program is just for the example in Chap3 of <<biological sequence anlysis>> to prediction the fair or load dices
'''
if __name__ == '__main__':
	if len(sys.argv) != 2:
		print 'usage: python Viterbi.py sequence.fa'
		sys.exit(0)
	print sys.argv
	sequence_file = sys.argv[1]
	O,S,Y,A,B,PI,Y_state = generate_data(sequence_file)
	n_state = len(S)
	n_seq_observation = len(Y)
	T1 = np.ones((n_state,n_seq_observation+1))*100
	T2 = np.ones((n_state,n_seq_observation+1))*100
	for i in range(n_state):
		if i == 0:
			T1[i][0] = 1
		else:
			T1[i][0] = 0
		T2[i][0] = 0
	for i in range(n_seq_observation+1):
		if i == 0:
			continue
		for l in range(n_state):
			max_1 = -125
			for k in range(n_state):
				if T1[k][i-1]*A[k][l]*B[l][int(Y[i-1])-1] > max_1:
					T1[l][i] = T1[k][i-1]*A[k][l]*B[l][int(Y[i-1])-1]
					max_1 = T1[k][i-1]*A[k][l]*B[l][int(Y[i-1])-1]
					T2[l][i] = k
	max_2 = -125
	for i in range(n_state):
		if i != 0:
			if T1[i][n_seq_observation] > max_2:
				max_2 = T1[i][n_seq_observation]
				zT = i
#	index = []
#	index.append(zT)
	XT = []
	XT.append(zT)
	for i in range(n_seq_observation):
		zT = T2[zT][n_seq_observation-i]
		XT.append(zT)
	X = []
	for i in range(n_seq_observation)[::-1]:
		X.append(XT[i])
	X_state = []
	for i in range(n_seq_observation):
		if X[i] <= 6:
			X_state.append('F')
		else:
			X_state.append('L')
	g = open('result.txt','w')
	g.write('Rolls:\t'+Y+'\n')
	g.write('Die:\t'+Y_state+'\n')
	g.write('Pred:\t'+''.join(X_state))
	g.close()
	print len(X_state)
#	print X
#	print XT
#	print zT
#	print T2
#	for i in range(n_state):
#		print T2[i][8]
#		print T2[i][300]





















