#!/home/bixichao/bin/python 
import sys
import os
import numpy as np
'''
	generate O,S,Y,A,B,PI
'''
def generate_data(a):
########################################
#
########################################
		O = [1,2,3,4,5,6]
		S = [0,1,2,3,4,5,6,7,8,9,10,11,12]
		Sequence_file = open(a)
		Roll = []
		Die = []
		write = False
        	for i in Sequence_file:
        	        for j in i:
        	                if j == '\t':
        	                        print 'new record is writting'
        	                        write = True
        	                        continue
        	                if write:
        	                        if i[0] == 'R':
        	                                if j == '\n':
        	                                        write = False
        	                                else:
        	                                        Roll.append(j)
        	                        if i[0] == 'D':
        	                                if j == '\n':
        	                                        write = False
        	                                else:
        	                                        Die.append(j)
		Sequence_file.close()
		Y = ''.join(Roll)
		Y_true = ''.join(Die)
		state_F = {}
		state_L = {}
		for i in O:
			state_F[i] = 1./6
			if i != 6:
				state_L[i] = 1./10
			else:
				state_L[i] = 1./2
		F_to_L = 0.05
		L_to_F = 0.1
		n_state = len(S)
		A = np.zeros((n_state,n_state))
		for i in range(n_state):
			if i == 0:
				A[i][0] = 0
			else:
				A[i][0] = 0
				A[0][i] = 1./(n_state-1)
		for i in range(n_state):
			if i != 0:
				for j in range(n_state):
					if j != 0 :
						if i in state_F:
							if j in state_F:
								A[i][j] = (1-F_to_L)*state_F[j]
							else:
								A[i][j] = F_to_L*state_L[j-6]
						else:
							if j in state_F:
								A[i][j] = L_to_F*state_F[j]
							else:
								A[i][j] = (1-L_to_F)*state_L[j-6]

		n_observation = len(O)
		B = np.zeros((n_state,n_observation))
		for i in range(n_state):
			if i !=0:
				for j in range(n_observation):
					if (i-1) == j or (i-7) == j:
						B[i][j] = 1
		PI = np.ones((n_state,1))*(1./(n_state-1))
		PI[0] = 0
		return O,S,Y,A,B,PI,Y_true
O,S,Y,A,B,PI,Y_true = generate_data('Sequence_dices.fa')
print O#---right
print S#---right
print Y#---right
print A#---right	
print B#---right
print PI#---right
print Y_true#---right
	
	



























