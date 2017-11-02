import numpy as np

#dpoints = image data points with feature values.

def fitness(sset, nofeat, noclus):
    clussize = np.zeroes(noclus)
    cluselem = np.zeroes((noclus,dpoints.shape[0]))
    cluselem = -1

    for i in range(dpoints.shape[0]):
        minval = ()
        clusindex = -1
        for j in range(noclus):
            val = 0 
            for k in range(nofeat):
                val += (dpoints[k] - sset[j][k]) ** 2
            if val < minval :
                minval = val
                clusindex = j
        cluselem[clusindex][clussize[clusindex]++] = i

    fitness = 0 

    for i in range(noclus):
        cluscenter = sset[i]
        for j in clussize[i]:
            val = 0
            dpoint = dpoints[j]
            for k in range(nofeat):
                val += (dpoint[k] - cluscenter[k]) ** 2
        val = val ** 0.5
        val /= clussize[i]
        fitness += val
    return fitness

def pso(feat_set, nofeat, noclus, seval):
    
    ''' 
        feat_set contains nofeat values for each cluster. Each value defines range of ith feature in its cluster.
        noclus = no of clusters.
        nofeat = no of features in a each cluster.
        seval = start and end values of features for partucular cluster.
    '''

    fdtype = ''
    for i in range(nofeat) :
        fdtype += feat_set[i].dtype.name + ','
    fdtype = fdtype[:len(fdtype)-1]

    max_iterations = 50
    noposs = 50 # no. of possible solutions
    poss_sols = np.zeroes((noposs, noclus), dtype=fdtype) # particles position
    pbest = np.zeroes((noposs, noclus), dtype=fdtype) # each particle's best position
    pfit = np.zeroes(noposs, dtype=float) # each particle's best fitness value
    gbest = np.zeroes(noclus, dtype=fdtype) # globally best particle postition
    parvel = np.zeroes((noposs, noclus), dtype=fdtype) # particle velocity
    c2 = 2 # social constant
    c1 = 1 # cognitive constant
    w = .4 # inertia  

    for i in range(noposs):
        for j in range(noclus):
            for k in range(nofeat):
                poss_sols[i][j][k] = np.random.randint(seval[j][k][0], high=seval[j][k][1]+1, dtype=feat_set[k].dtype.name)
                parvel[i][j][k] = np.random.randint(seval[j][k][0], high=seval[j][k][1]+1, dtype=feat_set[k].dtype.name)

    for it in range(max_iterations):
        for i in range(noposs):
            cur_par_fitness = fitness(poss_sols[i])
            best_fitness = fitness(pbest[i]);
            if cur_par_fitness < best_fitness:
                pfit[i] = best_fitness
                pbest[i] = poss_sols[i]

        global_fitness = fitness(gbest)
        
        for i in range(noposs):
            if pfit[i] < global_fitness:
                global_fitness = pfit[i]
                gbest = pfit[i]
        
        for i in range(noposs):
            for j in range(noclus):
            
                r1 = np.random.random_sample()
                r2 = np.random.random_sample()

                for k in range(nofeat):
                    
                    lb = seval[j][k][0]  
                    ub = seval[j][k][1] 
                    
                    inertial_vel = w * parvel[i][j][k] # inertia weight
                    cog_vel = r1 * c1 * (pbest[i][j][k] - poss_sols[i][j][k]) # cognitive factor
                    soc_vel = r2 * c2 * (gbest[j][k] - poss_sols[i][j][k]) # social factor

                    vel = inertial_vel + cog_vel + soc_vel #update in vel

                    if vel < lb || vel > ub:
                        vel = np.random.randint(lb,high = ub+1,dtype = feat_set[k].dtype.name)

                    perval[i][j][k] = vel
                    position = poss_sols[i][j][k] + vel 

                    if position < lb || position > ub:
                        position = np.random.randint(lb,high = ub+1,dtype = feat_set[k].dtype.name)
                    
                    poss_sols[i][j][k] = position #update in position



        
