# This file contains the code for the implementation of the Simulated Annealing.
# This file is written by Ruomeng Xu
import math
import random
import time

def score_tsp(dis_mat,tsp_tour):
	#given a tsp tour, return its length (for computing initial tsp)
	tour_length=0
	for i in range(len(tsp_tour)-1):
		tour_length=tour_length+dis_mat[tsp_tour[i],tsp_tour[i+1]]
	return tour_length	

def get_random(city_num):
	#for 2-opt exchange, generate a random 2-opt exchange
	r1,r2=random.sample(range(1,city_num),2)
	if r1<r2:
		return [r1,r2]
	else:
		return [r2,r1]

def neighbor2opt(dis_mat,tsp_current,score_current,index):
	#compute the 2-opt neighbor and its score
	i=index[0]
	j=index[1]
	tsp_neighbor=tsp_current[:i]
	tsp_neighbor.extend(tsp_current[j:i-1:-1])
	tsp_neighbor.extend(tsp_current[j+1:])
	delete=dis_mat[tsp_current[i],tsp_current[i-1]]+dis_mat[tsp_current[j],tsp_current[j+1]]
	add=dis_mat[tsp_current[i-1],tsp_current[j]]+dis_mat[tsp_current[i],tsp_current[j+1]]
	score_neighbor=score_current-delete+add
	return tsp_neighbor,score_neighbor


def pro(score_current,score_neighbor,T):
	#compute pro
	if score_neighbor<score_current:
		return 1
	else:
		return math.exp(1.0*(score_current-score_neighbor)/T)

def simulated_annealing(dis_mat,initial_T,alpha,min_T,seed,cutoff):
	random.seed(seed)
	city_num=int(math.sqrt(len(dis_mat)))
	tsp_current=random.sample(range(0,city_num),city_num)
	tsp_current.append(tsp_current[0])
	score_current=score_tsp(dis_mat,tsp_current)
	trace=[(0,score_current)]
	T=initial_T
	diff_time=0
	begin_time=time.time()
	while T>min_T and float(cutoff)>diff_time:
		index=get_random(city_num)
		tsp_neighbor,score_neighbor=neighbor2opt(dis_mat,tsp_current,score_current,index)
		p=pro(score_current,score_neighbor,T)
		if random.random()<=p:
			tsp_current=tsp_neighbor
			score_current=score_neighbor
			T=T*alpha
			if score_current<trace[-1][1]:
				trace.append([time.time()-begin_time,score_current])
		diff_time=time.time()-begin_time
	return tsp_current,score_current,trace
