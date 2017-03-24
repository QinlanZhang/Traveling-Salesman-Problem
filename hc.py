# This file contains the code for the implementation of the Hill Climbing.
# This file is written by Chongwu Guo.
import numpy as np
import math
import time

import matplotlib.pyplot as plt

def readData(filename):
    filename = 'DATA/'+ filename
    f = open(filename,'r')
    line = f.readline()
    line = f.readline()
    line = f.readline().split()
    dimension = int( line[1])
    cities = []
 
    citycoors = [[0 for x in range(2)] for y in range(dimension)] 
    distMatrix = [[0 for x in range(dimension)] for y in range(dimension)] 
    f.readline()
    f.readline()
    for i in range(0,dimension):
        line = f.readline().split()
        citycoors[i][0] = int(float(line[1]))
        citycoors[i][1] = int(float(line[2]))
        cities.append(int(line[0])-1)

    for i in range(dimension):
        for j in range(dimension):
            distMatrix[i][j] = math.sqrt( (citycoors[i][0] - citycoors[j][0]) **2 + (citycoors[i][1] - citycoors[j][1])**2 )

    return cities,distMatrix

def createCityPermutation(cities,seed):

    np.random.seed(seed)
    citiesPerm = np.random.permutation(cities)
    citiesPerm = np.append(citiesPerm, citiesPerm[0])
    return citiesPerm

def totalCost(citiesPerm,distMatrix):
    cost = 0
    for i in range(len(citiesPerm)-1):
        cost += distMatrix[citiesPerm[i]][citiesPerm[i+1]]
    return cost

def Hill_Climbing(filename,cutoff,randseed):
    randseed = int (randseed)
    #cutoff = int (cutoff)
    cities,distMatrix = readData(filename)
    citiesPerm = createCityPermutation(cities,randseed)
    
    bestCost = totalCost(citiesPerm,distMatrix)
    best_time_score=[[0,int(bestCost)]]
    
    start = time.time()
    elapsed = 0
    while(elapsed < cutoff):
        while True:
            minchange = 0
            for i in range(0,len(cities)-2):
                for j in range(i+2,len(cities)):
                    change = (distMatrix[citiesPerm[i]][citiesPerm[j]] 
                              + distMatrix[citiesPerm[i+1]][citiesPerm[j+1]]
                              - distMatrix[citiesPerm[i]][citiesPerm[i+1]]
                              - distMatrix[citiesPerm[j]][citiesPerm[j+1]]
                              )
                    if(minchange > change ):
                        minchange = change
                        
                        min_i = i
                        min_j = j
            citiesPerm = twoOptSwap(citiesPerm,min_i,min_j)
       
            bestCost += minchange
            endTime = time.time()
            elapsed = endTime - start
            #print elapsed
            best_time_score.append([  endTime - start,int(bestCost)   ])
            if minchange >= -0.1:
                citiesPerm = rearrange(citiesPerm)
                return int(bestCost), citiesPerm, best_time_score
    if(elapsed >= cutoff):
        
        return int(bestCost), citiesPerm, best_time_score


def rearrange(citiesPerm):
###################### rearrange the result so it starts with 0  ##############
    citiesPermX = citiesPerm[0:-1]

    for w in range(len(citiesPermX)):
        if citiesPermX[w] == 0:
            zeroIndex = w
            break
        
    firstHalf = citiesPermX[zeroIndex:]
    secondHalf = citiesPermX[0:zeroIndex]
    permStartWithZero = np.append(firstHalf, secondHalf)
    permStartWithZero = np.append(permStartWithZero,0)
    return permStartWithZero
    
def twoOptSwap(citiesPerm,i,j):

    newCitiesPerm = citiesPerm[:]
    newCitiesPerm[i+1:j+1] = citiesPerm[j:i:-1]
    return newCitiesPerm

