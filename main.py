from sa import *
import sys
from fi import *
from hc import *
from bnb import *
from MSTapproximation import *
import math
import os
def readfile(filename):
	#read file from DATA/XXX.tsp
	#return a list of coordinate
	filename = 'DATA/'+ filename
	tspinfo = [];
	with open(filename) as file:
		for line in file.readlines()[5:]:
			if line.strip() == "EOF":
				break
			else:
				i,x,y=line.strip().split(' ')
				tspinfo.append((float(x),float(y)))
	
	
	return tspinfo

def dis_matrix(tspinfo):
	#create distance matrix  
	#return a n\times n distance matrix
	dis_mat={}
	for i,(x1,y1) in enumerate(tspinfo):
		for j,(x2,y2) in enumerate(tspinfo):
			dx=x1-x2
			dy=y1-y2
			dis_mat[i,j]=round(math.sqrt(dx*dx+dy*dy))
	return dis_mat

def output(output_file,tsp_tour,tsp_score,trace,dis_mat):
	#output
	


	DIR = 'OUTPUT/'
	if not os.path.exists(DIR):
			os.makedirs(DIR)
	
	sol_file = open(DIR + output_file + '.sol','w')
	trace_file = open(DIR + output_file + '.trace','w')
	sol_file.write(str(int(tsp_score))+'\n')
	for i in range(len(tsp_tour)-1):
		length=int(dis_mat[tsp_tour[i],tsp_tour[i+1]])
		sol_file.write(str(tsp_tour[i]) + ' ' + str(tsp_tour[i+1]) + ' ' + str(length) + '\n' )
	
	sol_file.close()
	for (time,score) in trace:
		trace_file.write(str(format(time,'.2f')) + ', ' + str(int(score)) + '\n')
	trace_file.close()

def main():
	#run : python main.py filename method cutoff seed
	#example:python main.py Atlanta LS2 600 1
	num_args = len(sys.argv)
	if num_args < 5:
		print ("error: not enough input arguments")
		exit(1)
	filename = sys.argv[1]
	method = sys.argv[2]
	cutoff = sys.argv[3]
	seed = sys.argv[4]
	tspinfo = readfile(filename)
	dis_mat = dis_matrix(tspinfo)
	output_file = filename[:len(filename)-4] + '_' + method + '_' + cutoff
	
	if method == 'LS1':
		#Simulated Annealing + 2opt
		output_file = output_file + '_' + seed
		initial_T=1000000
		alpha=0.999
		min_T=10**(-6)
		tsp_tour,tsp_score,trace = simulated_annealing(dis_mat,initial_T,alpha,min_T,int(seed),cutoff)
		output(output_file,tsp_tour,tsp_score,trace,dis_mat)

	elif method == 'Heur':
		#Farthest Insertion
		tsp_tour,tsp_score,trace=FarthestInsertion(dis_mat)
		output(output_file,tsp_tour,tsp_score,trace,dis_mat)
	elif method == 'MSTApprox':
		run_time,tsp_score=run_MSTApprox(filename,cutoff)
	elif method == 'LS2':
		tsp_score,tsp_tour,trace = Hill_Climbing(filename,cutoff,int(seed))
		output_file=output_file+'_'+seed
		output(output_file,tsp_tour,tsp_score,trace,dis_mat)
	elif method == 'BnB':
		tsp_tour,tsp_score,trace = BnB(filename, cutoff)
		output(output_file,tsp_tour,tsp_score,trace,dis_mat)
	else:
 		print('ERROR: NO METHOD FOUND')
 		exit(1)

if __name__ == '__main__':
    # run the experiments
    main()

