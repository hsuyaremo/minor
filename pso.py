import numpy as np
import sys

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

def pso(nofeat, noclus, seval, dpoints):
    
    ''' 
        noclus = no of clusters.
        nofeat = no of features in a each cluster.
        seval = start and end values of features for partucular cluster.
    '''
    randomcount = 0
    max_iterations = 10
    noposs = 5 # no. of possible solutions
    poss_sols = np.zeros((noposs, noclus, nofeat),) # particles position
    pbest = np.zeros((noposs, noclus, nofeat),) # each particle's best position
    pfit = np.zeros(noposs,) # each particle's best fitness value
    gbest = np.zeros((noclus, nofeat),) # globally best particle postition
    parvel = np.zeros((noposs, noclus,nofeat),) # particle velocity
    c2 = 2 # social constant
    c1 = 1 # cognitive constant
    w = .4 # inertia  
    global_fitness = sys.maxint

    for i in range(noposs):
        pfit[i] = sys.maxint
        
    for i in range(noposs):
        for j in range(noclus):
            for k in range(nofeat):
                poss_sols[i][j][k] = np.random.randint(seval[j][k][0], high=seval[j][k][1]+1)
        print "random generated",poss_sols[i]

    for it in range(max_iterations):
        for i in range(noposs):
            cur_par_fitness = fitness(poss_sols[i], nofeat, noclus, dpoints)
            best_fitness = pfit[i]
            if cur_par_fitness < best_fitness:
                pfit[i] = cur_par_fitness
                pbest[i] = poss_sols[i]
     
        for i in range(noposs):
            if pfit[i] < global_fitness:
                global_fitness = pfit[i]
                gbest = poss_sols[i]

        for i in range(noposs):
            for j in range(noclus):
            
                r1 = np.random.random_sample()
                r2 = np.random.random_sample()

                for k in range(nofeat):
                    
                    lb = 0
                    ub = 260
                    
                    inertial_vel = w * parvel[i][j][k] # inertia weight
                    cog_vel = r1 * c1 * (pbest[i][j][k] - poss_sols[i][j][k]) # cognitive factor
                    soc_vel = r2 * c2 * (gbest[j][k] - poss_sols[i][j][k]) # social factor

                    vel = inertial_vel + cog_vel + soc_vel #update in vel

                    if vel < lb or vel > ub:
                        vel = np.random.randint(lb,high = ub+1)
                        randomcount += 1

                    parvel[i][j][k] = vel
                    position = poss_sols[i][j][k] + vel 

                    if position < lb or position > ub:
                        position = np.random.randint(lb,high = ub+1)
                    
                    poss_sols[i][j][k] = position #update in position

    print randomcount
    
    
    fitnessi, cluselem, clussize = fitness(gbest, nofeat, noclus, dpoints, tr=0)
    return gbest, cluselem, clussize
        
