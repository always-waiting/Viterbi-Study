#!/home/bixichao/bin/python 
from __future__ import division
import sys
import os
import numpy as np
from Package_for_Baum_Welch import generate_data
from Package_for_Baum_Welch import backward
from Package_for_Baum_Welch import forward
from Package_for_Baum_Welch import logPx
from Package_for_Baum_Welch import AE
from Package_for_Baum_Welch import PI_cal
'''
	parameter illusion:
		O
		S
		A
		B
		PI
		Y
'''
if __name__ == '__main__':
	if len(sys.argv) != 2:
		print 'usage wrong!!!'
		sys.exit(0)
	print sys.argv
	sequence_file = sys.argv[1]
	O,S,Y,A_pre,B_pre,PI_pre,Y_true = generate_data(sequence_file)
#	print O,'\n',S,'\n',A_pre,'\n',B_pre,'\n',PI,'\n',Y,'\n',Y_true#---right
	threshold = 1e-200
	cycle_max = 1000
	count_cycle = 0
	loop = True
	while loop:
		count_cycle = count_cycle + 1
		F_pre = forward(Y,A_pre,B_pre,PI_pre)
		b_pre = backward(Y,A_pre,B_pre,PI_pre)
		A_next,B_next,Px_log2_pre = AE(F_pre,b_pre,Y,A_pre,B_pre)
		PI_next = PI_cal(A_next)
		Px_log2_next = logPx(Y,A_next,B_next,PI_next)
		if abs(Px_log2_pre-Px_log2_next) > threshold:
			A_pre = A_next
			B_pre = B_next
			PI_pre = PI_next
		else:
			loop = False
			A_pre = A_next
			B_pre = B_next
			PI_pre = PI_next
		if count_cycle == cycle_max:
			break
	print A_pre
	print '@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@'
	print B_pre
	print '@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@'
	print count_cycle
	print '@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@'
#	print Px_log2_pre
	print '@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@'
#	print Px_log2_next





















