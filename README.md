# Traveling-Salesman-Problem
INTRODUCTION
- - - - - - - - - - - - - -
The main.py proves code for parsing the .tsp file(readfile(filename)), computing solution for given TSP with 5 different algorithms(Branch & Bound, Simulated Annealing, Hill Climbing, MST Approximation, Farthest Insertion), and generating an solution file as well as a trace file (output()).
The bnb.py tackle TSP by Branch & Bound algorithm
The fi.py tackle TSP by Farthest Insertion algorithm
The hc.py tackle TSP by Hill Climbing algorithm
The sa.py tackle TSP by Simulated Annealing algorithm
The MSTApproximation.py tackle TSP by MST Approximation algorithm



HOW TO RUN
- - - - - - - - - - - - - -
python main.py instance method cutoff seed
e.g. python main.py Atlanta.tsp LS2 600 10

instance: filename
method: BnB|MSTApprox|Heur|LS1|LS2
cutoff: cutoff time in seconds
seed: random seed

DO NOT USE "python3 main.py instance method cutoff seed”
Please check whether the INSTANCE FILE is in DATA folder before
running it!



FUNCTION AND EXPLANATION
- - - - - - - - - - - - - -
readfile(filename)
readfile: parse .tsp
Input: filename = XXX.tsp
Output: tspinfo = coordinate information of all vertices

output(output_file,tsp_tour,tsp_score,trace,dis_mat)
output: generating a solution file as well as a trace file and put it into OUTPUT folder
Input: output_file = file name < instance >_< method >_< cutoff >(_< randSeed >).sol, e.g. Atlanta_LS2_600_2001.sol
       tsp_tour = a solution (a sequence of vertices) for tsp
       tsp_score = the length of solution
       trace = trace, a list of list [time, score]
       dis_mat = disnatce matrix of given instance
Output: file = solution file and trace file

dis_matrix(tspinfo)
dis_matrix: compute the distance between any two vertices and keep the information as matrix
Input: tsp_info = coordinate information of a given instance
Output: distance matrix of a given instance

simulated_annealing(dis_mat,initial_T,alpha,min_T,seed,cutoff)
simulated_annealing: yield a solution by simulated annealing
Input: dis_mat = distance matrix of a given instance
       initial_T, alpha, min_T = cooling schedule 
       seed = random seed
       cutoff = cutoff time
Output: tsp_tour = solution
        tsp_score = length of solution
        trace = trace information

FarthestInsertion(dis_mat)
FarthestInsertion: yield a solution by farthest insertion
Input: dis_mat = distance matrix of a given instance
Output: tsp_tour = solution
        tsp_score = length of solution
        trace = trace information

run_MSTApprox(filename,cutoff)
run_MSTApprox: yield a solution by MST Approximation
Input: filename = file name of a given instance
       cutoff = cutoff time
Output: run_time = running time of the algorithm
        tsp_score = the length of solution


Hill_Climbing(filename,cutoff,seed)
Hill_Climbing: yield a solution by Hill Climbing
Input: filename = file name of a given instance
       cutoff = cutoff time
       seed = random seed
Output: tsp_tour = solution
        tsp_score = length of solution
        trace = trace information

BnB(filename, cutoff)
BnB: yield a solution by Branch and Bound
Input: filename = file name of a given instance
       cutoff = cutoff time
Output: tsp_tour = solution
        tsp_score = length of solution
        trace = trace information

