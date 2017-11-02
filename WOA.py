import numpy as np

# dpoints

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

    fitness += val ** 0.5
    return fitness

def woa(feat_set, nofeat, noclus, seval):
    
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
    poss_sols = np.zeroes((noposs, noclus), dtype=fdtype) # whale positions
    pbest = np.zeroes((noposs, noclus), dtype=fdtype) # each whale's best positions
    pfit = np.zeroes(noposs, dtype=float) # each whale's fitness values
    gbest = np.zeroes(noclus, dtype=fdtype) # globally best wahle postitions
    b = 2

    for i in range(noposs):
        for j in range(noclus):
            for k in range(nofeat):
                poss_sols[i][j][k] = np.random.randint(seval[j][0], high=seval[j][1]+1, dtype=feat_set[k].dtype.name)

    global_fitness = fitness(gbest)

    for i in range(noposs):
        cur_par_fitness = fitness(poss_sols[i])
        if cur_par_fitness < best_fitness:
            global_fitness = best_fitness
            gbest = poss_sols[i]

    for it in range(max_iterations):
    	for i in range(noposs):
    		a = 2 - 2*it/max_iterations
    		r = np.random.random_sample()
    		A = 2*a*r - a
    		C = 2*r
    		l = np.random.random_sample()
    		p = np.random.random_sample()
			for j in range(noclus):
				for k in range(nofeat):
					ub = seval[j][k][1]
					lb = seval[j][k][0]
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
						updatedx = D * math.exp(b*l) * math.cos(2* math.acos(-1) * l) + _x

					if updatedx > ub || updatedx < lb:
						updatedx = np.random.randint(lb, high = ub+1, dtype = feat_set[k].dtype.name)

					poss_sols[i][j][k] = updatedx
			
			fitnessi = fitness(poss_sols[i]);
			if fitnessi < global_fitness :
				global_fitness = fitnessi
				gbest = poss_sols[i] 
	
