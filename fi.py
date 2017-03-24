# This file contains the code for the implementation of the Farthest Insertion.
# This file is written by Ruomeng Xu

import math
import time
import numpy

def FindFarthest(dis_mat,partial_tour):
	#Find the unselected vertex whose minimal distance to the partial tour is maximal
	city_num=int(math.sqrt(len(dis_mat)))
	maxdis=-1
	maxindex=-1
	for i in range(city_num):
		if i not in partial_tour:
			dis_list=[dis_mat[i,j] for j in partial_tour]
			dis=min(dis_list)
			if dis>maxdis:
				maxdis=dis
				maxindex=i
	return maxindex

def FindInsertion(dis_mat,partial_tour,vertex):
	#Find the insertation location which minimize the increment of partial tour
	mindis=numpy.inf
	minindex=-1
	for i,index1 in enumerate(partial_tour[:-1]):
		index2=partial_tour[i+1]
		dis=dis_mat[index1,vertex]+dis_mat[vertex,index2]-dis_mat[index1,index2]
		if dis<mindis:
			mindis=dis
			minindex=i
	return minindex,mindis

def FarthestInsertion(dis_mat):
	#Given the distance matrix, implement Farthest Insertion
	#Use [0,0] as initial partial tour
	#No need to use cutoff time and seed
	city_num=int(math.sqrt(len(dis_mat)))
	partial_tour=[0,0]
	partial_tour_score=0
	begin_time=time.time()
	trace=[]
	while len(partial_tour)!=city_num+1:
		insert_vertex=FindFarthest(dis_mat,partial_tour)
		insert_location,delta_score=FindInsertion(dis_mat,partial_tour,insert_vertex)
		new_partial_tour=partial_tour[:insert_location+1]
		new_partial_tour.append(insert_vertex)
		new_partial_tour.extend(partial_tour[insert_location+1:])
		partial_tour_score=partial_tour_score+delta_score
		partial_tour=new_partial_tour
	trace.append([time.time()-begin_time,partial_tour_score])
	return partial_tour,partial_tour_score,trace

