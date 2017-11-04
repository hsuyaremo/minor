import numpy as np
import math
import sys

# dpoints

def fitness(sset, nofeat, noclus, dpoints, tr=1,):
    clussize = np.zeros(noclus, dtype=int)
    cluselem = np.zeros((noclus,dpoints.shape[0]), dtype=int)

    for i in range(dpoints.shape[0]):
        minval = sys.maxint
        clusindex = -1
        for j in range(noclus):
            val = 0.0
            for k in range(nofeat):
                val += (dpoints[i][k] - sset[j][k]) ** 2.0
            if val < minval :
                minval = val
                clusindex = j
        cluselem[clusindex][clussize[clusindex]] = i
        clussize[clusindex] += 1;

    fitness = 0 

    for i in range(noclus):
        cluscenter = sset[i]
        val = 0.0
        for j in range(clussize[i]):
            dpoint = dpoints[cluselem[i][j]]
            for k in range(nofeat):
                val += (dpoint[k] - cluscenter[k]) ** 2.0
        val = val ** 0.5
        if clussize[i] > 0:
            val /= clussize[i]
        fitness += val
    
    if tr :
        return fitness
    else :
        return fitness, cluselem, clussize

def woa(nofeat, noclus, seval ,dpoints):
    
    ''' 
        noclus = no of clusters.
        nofeat = no of features in a each cluster.
        seval = start and end values of features for partucular cluster.
    '''
    randomcount=0
    max_iterations = 10
    noposs = 5 # no. of possible solutions
    poss_sols = np.zeros((noposs, noclus, nofeat)) # whale positions
    gbest = np.zeros((noclus, nofeat)) # globally best wahle postitions
    b = 2.0

    for i in range(noposs):
        for j in range(noclus):
            for k in range(nofeat):
                poss_sols[i][j][k] = np.random.randint(seval[j][k][0], high=seval[j][k][1]+1)

    global_fitness = fitness(gbest, nofeat, noclus, dpoints)
    
    for i in range(noposs):
        cur_par_fitness = fitness(poss_sols[i], nofeat, noclus, dpoints)
        print cur_par_fitness,
        if cur_par_fitness < global_fitness:
            global_fitness = cur_par_fitness
            gbest = poss_sols[i]

    print "initial gfitness=",global_fitness
    for it in range(max_iterations):
        for i in range(noposs):
            a = 2.0 - (2.0*it)/(1.0 * max_iterations)
            r = np.random.random_sample()
            A = 2.0*a*r - a
            C = 2.0*r
            l = 2.0 * np.random.random_sample() - 1.0
            p = np.random.random_sample()
            for j in range(noclus):
                for k in range(nofeat):
                    lb = 0
                    ub = 260

                    x = poss_sols[i][j][k]
                    if p < 0.5:
                        if abs(A) < 1:
                            _x = gbest[j][k]
                        else :
                            rand = np.random.randint(noposs)
                            _x = poss_sols[rand][j][k]

                        D = abs(C*_x - x)
                        updatedx = _x - A*D
                    else :
                        _x = gbest[j][k]
                        D = abs(_x - x)
                        updatedx = D * math.exp(b*l) * math.cos(2.0* math.acos(-1.0) * l) + _x

                    if updatedx > ub or updatedx < lb:
                        updatedx = np.random.randint(lb, high = ub+1)
                        randomcount += 1

                    poss_sols[i][j][k] = updatedx

            fitnessi = fitness(poss_sols[i], nofeat, noclus, dpoints)
            if fitnessi < global_fitness :
                global_fitness = fitnessi
                gbest = poss_sols[i]
                
    print randomcount
    fitnessi, cluselem, clussize = fitness(gbest, nofeat, noclus, dpoints, tr=0)
    return gbest, cluselem, clussize
