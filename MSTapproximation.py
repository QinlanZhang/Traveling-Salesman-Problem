# This file contains the code for the implementation of the MST approximation.
# This file is written by Qinlan Zhang
import time
import networkx as nx
import random as random
import os
import math
import heapq
            

               
def run_MSTApprox(filename,cutofftime):
    DIR = 'OUTPUT/'
    if not os.path.exists(DIR):
        os.makedirs(DIR)
    G = nx.Graph()
    n_node,e_list=parseData(filename)
    adjacency_dict=parseEdges(e_list)
    MST,total_w=computeMST(adjacency_dict)
    G.add_weighted_edges_from(e_list)   
    file_name = str(filename[:-4]) + '_MSTApprox_'+str(cutofftime)+'.sol'
    file_name_trace=str(filename[:-4]) + '_MSTApprox_'+str(cutofftime)+'.trace'
    file2=open(DIR+file_name_trace,"w")
    t_start=time.time()
    starting_node=0
    opt_tour, opt_cost=approximation(G,file_name,e_list,starting_node)
    time_stamp=time.time()-t_start
    file2.write("{0:.2f}".format(time_stamp)+","+str(opt_cost)+"\n")
    for i in range(1,n_node):
        new_tour, new_cost=approximation(G,file_name,e_list,i)
        if opt_cost>new_cost:
            opt_tour,opt_cost=new_tour,new_cost
            time_stamp=time.time()-t_start
            file2.write("{0:.2f}".format(time_stamp)+","+str(opt_cost)+"\n")
            #print(opt_tour,opt_cost)         
    run_time=time.time()-t_start
    outputData(opt_tour,opt_cost,file_name,G)
    #print("runtime is"+str(run_time))
    #print("opt_cost is"+str(opt_cost))
    return run_time,opt_cost
 



def parseData(inputfile):
    inputfile="DATA/"+inputfile    
    input_file=open(inputfile)
    data=input_file.readlines()
    node_info=[]
    e_list=[]
    for line in data[5:]:
        if line!="EOF\n":
            n,lat,logt=line.split()
            n=int(n)
            lat=float(lat)
            logt=float(logt)
            node_info.append([n,lat,logt])
    n_node=len(node_info)
    for i in range(n_node):
        for j in range(i+1,n_node):
            node1=node_info[i]
            node2=node_info[j]
            dist=math.sqrt((node1[1] - node2[1]) ** 2 +(node1[2] - node2[2]) ** 2)
            e_list.append([i,j,round(dist)])
    return (n_node,e_list)
  #compute distance and generate the e_list containig all the (u,v,dist) info



def parseEdges(e_list):
    adjacency_dict={}
    for line in e_list:
        u,v,w=line
        if u not in adjacency_dict:
            adjacency_dict[u]=[(w,v)]
        else:
            adjacency_dict[u]=adjacency_dict[u]+[(w,v)]
        if v not in adjacency_dict:
            adjacency_dict[v]=[(w,u)]
        else:
            adjacency_dict[v]=adjacency_dict[v]+[(w,u)]
    return adjacency_dict




def computeMST(adjacency_dict):
    '''
     Compute the MST and total weight of MST from the whole (u,v,dist) info
    '''
    Q=[]
    S={}
    total_weight=0
    MST=[]
    key_list=list(adjacency_dict.keys())
    first_node=key_list[0]
    S[first_node]=1
    for item in adjacency_dict[first_node]:
        (w,v)=item
        u=first_node
        heapq.heappush(Q,(w,u,v))
    while len(Q)!=0:
        init_node=heapq.heappop(Q)
        next_node=init_node[2]
        if next_node not in S:
            S[next_node]=1
            MST.append(init_node)
            total_weight+=int(init_node[0])
            for sub_item in adjacency_dict[next_node]:
                (w_sub,v_sub)=sub_item
                u_sub=next_node
                heapq.heappush(Q,(w_sub,u_sub,v_sub))
    return MST,total_weight

        
def approximation(G,file_name,e_list,starting_node):
    '''
    This method takes in a graph and uses the MST approximation algorithm to
    find an approximate solution to TSP for a given tree.
    '''
    solution = _get_solution(G,e_list,starting_node)
    #solution is a path in the format(u,v,w), the output of get_path_edgelist, the input of get_tour
    tour = get_tour(solution)   
    cost = int(_get_solution_weights(solution)) 
    return tour, cost


def _get_solution(G,e_list,starting_node):
    '''
    This function computes the path_nodes from depth first search and use path_nodes and the whole edges of the graph
    to generate the corresponding results of get_path_edgelist function, which is used
    as the input of get_tour
    '''
    adjacency_list=parseEdges(e_list)
    MST_edge_list = computeMST(adjacency_list)[0]
    r_edgelist=[]
    f_edgelist=[]
    for e in MST_edge_list:
        forward_e=[e[1],e[2],e[0]]
        reverse_e=[e[2],e[1],e[0]]
        f_edgelist.append(forward_e)
        r_edgelist.append(reverse_e)
    edge_list =f_edgelist + r_edgelist

    #depth first search generate the path(denoted by the connected nodes)
    path_nodes = _depth_first_search(edge_list,starting_node)
    #print("PN:"+str(path_nodes))
    
    edge_list=G.edges(data=True)
  
    return _get_path_edge_list(path_nodes, edge_list)



def _get_solution_weights(solution):
    '''
    This function retuns the sum weights of a solution.
    '''
    weight = 0
    for edge in solution:
        weight += edge[2]
    return weight


def _get_path_edge_list(path_nodes, edge_list):
    '''
    This function get get the weights for the node path.
    '''
    #path is a list of nodes representing the path
    path = []
    n_nodes = len(path_nodes)
    #n_nodes is the number of nodes in path
    for edge in edge_list:
        for i in range(n_nodes):
            node_i = path_nodes[i]
            node_i_plus = path_nodes[(i + 1) % n_nodes]
            if edge[0] == node_i and edge[1] == node_i_plus:
                path.append((edge[0], edge[1], edge[2]["weight"]))
            elif edge[1] == node_i and edge[0] == node_i_plus:
                path.append((edge[1], edge[0], edge[2]["weight"]))
    # elements in path is in the form(u,v,w)
    #print("path is")
    #print(path)
    return path


def _depth_first_search(edge_list,starting_node):
    '''
    This function does a depth first search of a graph with a random node
    selected as the root of a tree representing the graph.
    '''
    G_tmp = nx.Graph()
    G_tmp.add_weighted_edges_from(edge_list)
    #start with a root node and perform depth first search
    path_sequence = list(nx.dfs_preorder_nodes(G_tmp,starting_node))
    return path_sequence





def get_tour(state):
    '''
    Get tour of graph starting with node v1, v2, v2, ..., vn, v1.
    '''
    node_list = _get_node_list(state)
    tour = [node_list[0]]
    for node in node_list[1:]:
        tour.append(node)
        tour.append(node)
    return tour[:-1]
    #return the euc_tour


def _get_node_list(state):
    tmp_state = state[:]
    first_edge = tmp_state.pop()
    node_list = [first_edge[0], first_edge[1]]
    while node_list.count(node_list[-1]) < 2:
        for edge in tmp_state:
            if edge[0] == node_list[-1]:
                tmp_state.remove(edge)
                node_list.append(edge[1])
            elif edge[1] == node_list[-1]:
                tmp_state.remove(edge)
                node_list.append(edge[0])
    return node_list


def outputData(tour,cost,outputfile,G):
    DIR = 'OUTPUT/'
    if not os.path.exists(DIR):
        os.makedirs(DIR)
    file=open(DIR+outputfile,"w")
    file.write(str(cost))
    file.write("\n")
    num=len(tour)
    i=0
    touroutput=[]
    while i<num-1:
        n1=tour[i]
        n2=tour[i+1]
        i=i+2
        for edge in G.edges(data=True):
            if edge[0]==n1 and edge[1]==n2:
                touroutput.append([str(n1),str(n2),str(int(edge[2]["weight"]))])
            elif edge[1]==n1 and edge[0]==n2:
                touroutput.append([str(n1),str(n2),str(int(edge[2]["weight"]))])
    for item in touroutput:
        file.write(item[0]+"\t"+item[1]+"\t"+item[2]+"\n")
    file.close()
    #print(touroutput)




       
    

