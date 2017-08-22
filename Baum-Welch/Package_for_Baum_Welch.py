#!/home/bixichao/bin/python 
import sys
import os
import numpy as np
import math
'''
	Input:	n_observation
		n_state
	Output: initial parameter for Baum-Welch algorithm
		O:	the observation space	n_observation*1
		S:	the state space		n_state*1
		A:	transition matrix	n_state*n_state
		B:	emission matrix		n_state*n_observation
		PI:	initial probabilities	n_state*1
'''
def generate_data(a):
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
	O = [1,2,3,4,5,6]
	S = [1,2,3,4,5,6,7,8,9,10,11,12]
	n_observation = len(O)
	n_state = len(S)
	A = np.zeros((n_state,n_state))
	p = 1./n_state
	for i in range(n_state):
		for j in range(n_state):
			A[i][j] = p
	B = np.zeros((n_state,n_observation))
	for i in range(n_state):
		for j in range(n_observation):
			if i == j:
				B[i][j] = 1
			if i == j+6:
				B[i][j] = 1
	PI = np.ones((n_state,1))*p
	return O,S,Y,A,B,PI,Y_true
########################################################
def forward(Y,A,B,PI):
	n_state,n_observation = B.shape
	n_seq_observation = len(Y)
	F = np.zeros((n_state,n_seq_observation))
	for i in range(n_state):
		F[i][0] =  B[i][int(Y[0])-1]*PI[i]
	for i in range(n_seq_observation):
		for l in range(n_state):
			for k in range(n_state):
				if i != 0:
					F[l][i] = F[l][i] + B[l][int(Y[i])-1]*F[k][i-1]*A[k][l]
	return F
###############################################################################
#from Viterbi_data import generate_data
#O,S,Y,A,B,PI,Y_true = generate_data('Sequence_dices.fa')
#F = forward(Y,A,B,PI)
#print O,'\n',S,'\n',A,'\n',B,'\n',PI,'\n',Y,'\n',Y_true
#count = 0#---right
#n_state = len(S)
#n_seq_observation = len(Y)
#for i in range(n_state):#---right
#	for j in range(n_seq_observation):#---right
#		if F[i][j] != 0:#---right
#			count = count + 1#---right
#			print F[i][j]#---right
#print '\n' + str(count)#---right
#for i in range(n_state):#---right
#	print F[i][0]   #---right#       
#for i in range(n_state):#---right
#	print F[i][1]#---right
#for i in range(n_state):#---right
#	print F[i][2]#---right
#for i in range(n_state):#---right
#	print F[i][n_seq_observation-1]#---right
#################################################################################
def backward(Y,A,B,PI):
	n_state,n_observation = B.shape
	n_seq_observation = len(Y)
	b = np.zeros((n_state,n_seq_observation))
	for k in range(n_state):
		b[k][n_seq_observation-1] = PI[k]*B[k][int(Y[n_seq_observation-1])-1]
	for i in range(n_seq_observation)[::-1]:
		for k in range(n_state):
			for l in range(n_state):
				if i != (n_seq_observation-1) :
					b[k][i] = b[k][i] + A[k][l]*B[l][int(Y[i+1])-1]*b[l][i+1]
	return b
##################################################################################
#from Viterbi_data import generate_data
#O,S,Y,A,B,PI,Y_true = generate_data('Sequence_dices.fa')
#b = backward(Y,A,B,PI)
#print O,'\n',S,'\n',A,'\n',B,'\n',PI,'\n',Y,'\n',Y_true
#count = 0#---right
#n_state = len(S)
#n_seq_observation = len(Y)
#for i in range(n_state):#---right
#	for j in range(n_seq_observation):#---right
#		if b[i][j] != 0:#---right
#			count = count + 1#---right
#			print b[i][j]#---right
#print '\n' + str(count)#---right#
#for i in range(n_state):#---right
#	print b[i][0]#---right#       
#for i in range(n_state):#---right
#	print b[i][1]#---right
#for i in range(n_state):#---right
#	print b[i][2]#---right
#for i in range(n_state):#---right
#	print b[i][n_seq_observation-1]#---right
##################################################################################
def AE(F,b,Y,A,B):
	n_seq_observation = len(Y)
	n_state,n_observation = B.shape
	A_prenext = np.zeros((n_state,n_state))
	B_prenext = np.zeros((n_state,n_observation))
	Px = 0
	for i in range(n_state):
		Px = Px + F[i][n_seq_observation-1]
	Px_log2 = math.log(Px,2)
	for k in range(n_state):
		for l in range(n_state):
			for i in range(n_seq_observation-1):
				A_prenext[k][l] = A_prenext[k][l] + F[k][i]*A[k][l]*B[l][int(Y[i+1])-1]*b[l][i+1]
	for k in range(n_state):
		for l in range(n_state):
			A_prenext[k][l] = A_prenext[k][l]/Px
	for k in range(n_state):
		for l in range(n_observation):
			for i in range(n_seq_observation):
				if (int(Y[i])-1) == l:
					B_prenext[k][l] = B_prenext[k][l] + F[k][i]*b[k][i]
	for k in range(n_state):
		for l in range(n_observation):
			B_prenext[k][l] = B_prenext[k][l]/Px
	A_next = np.zeros((n_state,n_state))
	B_next = np.zeros((n_state,n_observation))
	for k in range(n_state):
		for l in range(n_state):
			sum_Aprenext = 0
			for i in range(n_state):
				sum_Aprenext = sum_Aprenext + A_prenext[k][i]
			A_next[k][l] = A_prenext[k][l]/sum_Aprenext
	for k in range(n_state):
		for l in range(n_observation):
			sum_Bprenext = 0
			for i in range(n_observation):
				sum_Bprenext = sum_Bprenext + B_prenext[k][i]
			B_next[k][l] = B_prenext[k][l]/sum_Bprenext
	PI_return = np.zeros((n_state,1))##############################
#	for i in range(n_state):###########################
#		if i < 7:################################
#			F_to_F = 0#########################
#			for k in range(6):########################
#				F_to_F = F_to_F + A[0][k]#####################
#			PI_return[i] = 0.5*A[0][i]/F_to_F##################
#		else:####################################################
#			F_to_L = 0#################################################
#			for k in range(6):########################################
#				F_to_L = F_to_L + A[0][k+6]###########################
#			PI_return[i] = 0.5*A[0][i]/F_to_L##############################
	return A_next,B_next,Px_log2
#################################################################################
#A_next,B_next,Px_log2_pre = AE(F,b,Y,A,B)
#print A_next
#print B_next
#################################################################################
def PI_cal(A):
	n_state,fun = A.shape
	PI_return = np.zeros((n_state,1))
	for index in range(n_state):
		PI_return_mid = np.zeros((n_state,1))
		for i in range(n_state):
			if i < 7:
				F_to_F = 0
				for k in range(6):
					F_to_F = F_to_F + A[index][k]
				PI_return_mid[i] = 0.5*A[index][i]/F_to_F
			else:
				F_to_L = 0
				for k in range(6):
					F_to_L = F_to_L + A[index][k+6]
				PI_return_mid[i] = 0.5*A[index][i]/F_to_L
			PI_return[i] = PI_return_mid[i]/n_state + PI_return[i]
	return PI_return
#################################################################################
def logPx(Y,A,B,PI):
	n_state,n_observation = B.shape
	n_seq_observation = len(Y)
	F = np.zeros((n_state,n_seq_observation))
	for i in range(n_state):
		F[i][0] =  B[i][int(Y[0])-1]*PI[i]
	for i in range(n_seq_observation):
		for l in range(n_state):
			for k in range(n_state):
				if i != 0:
					F[l][i] = F[l][i] + B[l][int(Y[i])-1]*F[k][i-1]*A[k][l]
	Px = 0
	for i in range(n_state):
		Px = Px + F[i][n_seq_observation-1]
	Px_log2 = math.log(Px,2)
	return Px_log2
####################################################################################
#loop1
O,S,Y,A,B,PI,Y_true = generate_data('Sequence_dices.fa')
F = forward(Y,A,B,PI)
b = backward(Y,A,B,PI)
A_next,B_next,Px_log2_pre = AE(F,b,Y,A,B)
PI_next = PI_cal(A_next)
Px_log2_next = logPx(Y,A_next,B_next,PI_next)
#print (Px_log2_pre - Px_log2_next)
#print Px_log2_pre
#print Px_log2_next
#print A_next
#print B_next
#print PI_next
####################################################################################
#loop2
#print '@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@'
F_next = forward(Y,A_next,B_next,PI_next)
b_next = backward(Y,A_next,B_next,PI_next)
A_next2,B_next2,Px_log2_pre = AE(F_next,b_next,Y,A_next,B_next)
PI_next2 = PI_cal(A_next2)
Px_log2_next = logPx(Y,A_next2,B_next2,PI_next2)
#print (Px_log2_pre - Px_log2_next)
#print Px_log2_pre
#print Px_log2_next
#print A_next2
#print B_next2
#print PI_next2
#####################################################################################
#print '@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@'
F_next2 = forward(Y,A_next2,B_next2,PI_next2)
b_next2 = backward(Y,A_next2,B_next2,PI_next2)
A_next3,B_next3,Px_log2_pre = AE(F_next2,b_next2,Y,A_next2,B_next2)
PI_next3 = PI_cal(A_next3)
Px_log2_next = logPx(Y,A_next3,B_next3,PI_next3)
#print (Px_log2_pre - Px_log2_next)
#print Px_log2_pre
#print Px_log2_next
#print A_next3
#print B_next3
#print PI_next3
####################################################################################
#PI_next3_0 = PI_next3
#PI_next3_1 = PI_cal(A_next3,1)
#PI_next3_2 = PI_cal(A_next3,2)
#PI_next3_3 = PI_cal(A_next3,3)
#print PI_next3_0
#print PI_next3_1
#print PI_next3_2
#print PI_next3_3
#print (PI_next-PI_next2)
#print (PI_next2-PI_next3)

























