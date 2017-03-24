# This file contains the code for the implementation of the Branch and Bound.
# This file is written by Ankita Jain

import pandas as pd
import numpy as np
import time
import sys
import os
import string
import scipy as sp
import heapq as hq


'''
Algorithm Steps
1. Set an initial upper bound as infinity. A tighter upper bound can also be set through any of the heuristic or local search approach.
2. We maintain a priority queue to keep track of the unexplored solutions. Each tuple of the priority queue will have information about the number of unvisited nodes, lower bound associated to the current path and the current path itself. 
3. Pop a given unexplored solution from the priority queue
3.a If the popped solution is complete, then check whether the total cost of the tour is less than the upper bound. If it is, then update the upper bound cost and tour with this solution.
3.b If the popped solution is partial and its lower bound cost is less than the upper bound, we will further explore this branch. Through row-column reduction, we will compute the lower bound of each of the sub-problems that contains the current path and a new unvisited node. And push these into the priority queue.
4. Repeat step 3 until priority queue becomes empty or total execution time exceeds the cutoff time.
'''



#Parse input file and create coordinate dataframe
def parseInputFile(file_name):
    args={}
    input_file =  './DATA/' + file_name
    coordinates = pd.DataFrame(columns=['Latitude', 'Longitude'])
    index=0
    with open(input_file) as f:
        for line in f:
            if ':' in line: 
                key, value = line.split(':')
                args[string.strip(key)] = string.strip(value)
            elif 'EOF' not in line:
                params = line.split(' ')
                if(len(params)==3):
                    coordinates.loc[len(coordinates),:]= np.array([float(params[1]), float(params[2])])
                    index+=1                      
    return coordinates        

# Create adjacency matrix from the coordinates
def createCostMatrix(coordinates):
    z = np.array([[complex(coordinates.loc[c,'Latitude'], coordinates.loc[c,'Longitude']) for c in coordinates.index]])
    adj_matrix = abs(z-z.T)
    cost_matrix = np.matrix.round(adj_matrix)
    cost_matrix_df = pd.DataFrame(cost_matrix,index=coordinates.index.values,columns=coordinates.index.values)
    
    for i in cost_matrix_df.index:
        cost_matrix_df.ix[i,i]=float('inf')  
    return cost_matrix_df 


# Row-Col Reduction to compute lower bound    
def doRowColReduction(matrix):
    lower_bound=0
	# subtract min of each row from corresponding rows, update lower bound
    row_min=matrix.min(axis=1)
    row_min.replace(to_replace=float('inf'), value=0, inplace=True)
    lower_bound += row_min.sum()
    matrix=matrix.sub(row_min, axis=0)
    
	# subtract min of each columns from corresponding columns,update lower bound
    col_min=matrix.min(axis=0)
    col_min.replace(to_replace=float('inf'), value=0, inplace=True)
    lower_bound += col_min.sum()
    matrix=matrix.sub(col_min, axis=1)
    return matrix, lower_bound 

def BnB(file_name, cut_off=600):
    coordinates = parseInputFile(file_name)
    cost_matrix = createCostMatrix(coordinates)
    return myBnB(cost_matrix, coordinates, cut_off)

def myBnB(cost_matrix, coordinates, cut_off):
	#Track execution time
    start_time = time.time()
    end_time = start_time + float(cut_off)
    adj_matrix = cost_matrix.copy()
    
	
    trace_data=[]
    cur_path=[]
    priority_queue=[]
    cur_path.append(0)
	# Push node 0 as a root of the tree with 0 lower bound
    hq.heappush(priority_queue,(adj_matrix.shape[0]-1, 0, cur_path))
	#Set upper bound as infinity
    upper_bound=float('inf')
	
    while len(priority_queue)!=0 and time.time() < end_time:
	
		#Pop an item from priority queue with minimum no. of remaining nodes, lower bound and path
        rem_nodes, cur_cost, cur_path = hq.heappop(priority_queue)

		#if it is not a complete tour
        if len(cur_path)<len(coordinates.index):
			#if lower bound is less than upper bound then explore this branch
            if cur_cost < upper_bound:
                cur_mat = cost_matrix.copy()
				#online reduce matrix till the current path
                for i in range(1,len(cur_path)):
                        from_node = cur_path[i-1]
                        to_node = cur_path[i]
                        cur_mat.loc[:,to_node] = float('inf')
                        cur_mat.loc[from_node,:] = float('inf')
                        cur_mat.loc[to_node, from_node]=float('inf')
                        cur_mat, c_cost = doRowColReduction(cur_mat)
                from_node=cur_path[-1]
                nodes_not_visited =  [i for i in range(adj_matrix.shape[0]) if i not in cur_path]
				
				#for each unvisited node, find reduce cost matrix and push to priority queue
                for to_node in nodes_not_visited:
                            edge_cost = cur_mat.loc[from_node, to_node]
                            temp = cur_mat.copy() 
                            temp.loc[:,to_node] = float('inf')
                            temp.loc[from_node,:] = float('inf')
                            temp.loc[to_node, from_node]=float('inf')
                            temp, temp_cost = doRowColReduction(temp)
                            hq.heappush(priority_queue, (adj_matrix.shape[0]-len(cur_path)-1, cur_cost + temp_cost + edge_cost, cur_path + [to_node]))                           
        elif cur_cost < upper_bound:
            upper_bound = cur_cost
            path_ub=cur_path
            trace_data.append((time.time()-start_time,int(upper_bound)))
            
    return path_ub + [path_ub[0]], int(upper_bound), trace_data
    






if __name__ == "__main__":
    
    file_name="Atlanta.tsp"
    cut_off = 200
    
    BnB(file_name, cut_off)


