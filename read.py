import matplotlib.pyplot as plt
from sklearn.svm import SVC
import numpy as np
import cv2
import os
import pso
import WOA
import feature
import enhance
import cPickle

nofeat = 1 #no of features in each cluster

def getclus(images, noclus):
	for it,name in enumerate(images):
		piarr = cv2.imread(enhanced + name ,0)
		mask ,piarr = enhance.skstr(piarr)
		
		r = piarr.shape[0]
		ground = [27.5,72.5,110,142.5]
		col = [63,127,191,255]

		lst = []
		for i in range(r):
			for j in range(r):
				if mask[i][j] == 255:
					lst.append((i,j))

		masked_image = np.zeros((len(lst),nofeat))
		for ii in range(len(lst)):
			i, j = lst[ii]
			masked_image[ii] = piarr[i*r +j]

		print "clustering..with pso"
		gbest, cluselem , clussize = pso.pso(nofeat,noclus,masked_image)
		print "done with clustering."

		print "data points are:"
		for i,j in enumerate(clussize):
			print "cluster",i,"contains",j,"elements"
		print "global best \n",gbest

		setc = [0,0,0,0]
		for i in range(noclus):
			val = 256
			for j in range(noclus):
				if abs(gbest[i] - ground[j]) < val:
					val = abs(gbest[i] - ground[j])
					setc[i] = col[j]

		seg_imag = np.zeros((r,r),dtype = np.uint8)
		
		for i in range(noclus):
			for j in range(clussize[i]):
				ii, jj = lst[cluselem[i][j]]
				seg_imag[ii,jj] = setc[i]

		plt.imsave(testing+str(it)+"p.jpg",seg_imag,cmap = "gray")
		features = feature.feature_extraction(seg_imag)
		if it == 0:
			psofeatures = features
		else:
			psofeatures = np.append(psofeatures, features, axis =0 )

		print "clustering..with woa"
		gbest, cluselem , clussize = WOA.woa(nofeat,noclus,seval,masked_image)
		print "done with clustering."

		print "data points are:"
		for i,j in enumerate(clussize):
			print "cluster",i,"contains",j,"elements"
		print "global best \n",gbest

		for i in range(noclus):
			val = 256
			for j in range(noclus):
				if abs(gbest[i] - ground[j]) < val:
					val = abs(gbest[i] - ground[j])
					setc[i] = col[j]

		seg_imag = np.zeros((r,r),dtype = np.uint8)
		
		for i in range(noclus):
			for j in range(clussize[i]):
				ii, jj = lst[cluselem[i][j]]
				seg_imag[ii,jj] = setc[i]

		plt.imsave(testing+str(it)+"w.jpg",seg_imag,cmap ="gray")
		features = feature.feature_extraction(seg_imag)
		if it == 0:
			woafeatures = features
		else :
			woafeatures = np.append(woafeatures, features, axis =0 )

	return woafeatures,psofeatures

enhancedtumour = "D:\\enhanced\\"
enhancednontumour = "D:\\images\\"

#enhance.enhtumour()
#enhance.enhnontumour()

images = [image for image in os.listdir(enhancedtumour)]
noclus = 4 # for cerebrospinal fluid, white matter, grey matter, abnormality
woa ,pso = getclus(images, noclus)
target = [1 for i in range(len(images))]

images = [image for image in os.listdir(enhancednontumour)]
noclus = 3
woan ,pson = getclus(images, noclus)
targetn = [0 for i in range(len(images))]

for i in range(pson.shape[0]):
	pso = np.append(pso, pson[i], axis = 0)
	woa = np.append(woa, woan[i], axis = 0)
target = np.append(target,targetn)

clf_woa = SVC(kernel = "poly", degree = 2)
clf_woa.fit(woa, target)

with open('clf_woa.pkl','wb') as woaclf:
	cPickle.dump(clf_woa, woaclf)

# with open('clf_woa.pkl','rb') as woaclf:
# 	clf_woa = cPickle.load(woaclf)

clf_pso = SVC(kernel = "poly", degree = 2)
clf_pso.fit(pso, target)

with open('clf_pso.pkl','wb') as psoclf:
	cPickle.dump(clf_pso, woaclf)

