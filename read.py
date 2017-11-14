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

noclus = 4 #no of clusters
nofeat = 1 #no of features in each cluster
d = 2 #patch size 

def saveimg(clussize, cluselem, nm, it ):
	seg_imag = np.zeros((r,r),dtype = np.uint8)
	col = [50,125,200,255]
	
	for i in range(noclus):
		for j in range(clussize[i]):
			ii, jj = lst[cluselem[i][j]]
			seg_imag[ii*d:(ii+1)*d,jj*d:(jj+1)*d] = col[i]

	plt.imsave(testing+nm+str(it)+".jpg",seg_imag)

def getclus(images):
	for it,name in enumerate(images):
		piarr = cv2.imread(enhanced + name ,0)
		mask ,piarr, ls = enhance.skstr(piarr)
		
		r = piarr.shape[0]

		print "Processing image",name,"..."
		total_features = np.zeros((r/d*r/d,nofeat))
		for i in range(r/d):
			for j in range(r/d):
				roi = piarr[i*d:(i+1)*d,j*d:(j+1)*d]
				idx = i*r/d + j
				total_features[idx][0] = np.mean(roi)
		print "processing done."
		
		lst = []
		for i in range(r/d):
			for j in range(r/d):
				flag = 0
				maskroi = mask[i*d:(i+1)*d,j*d:(j+1)*d]
				for ii in range(d*d):
					if maskroi.flatten()[ii] == 255:
						flag =1
						break
				if flag == 1:
					maskroi[:] = 255
					lst.append((i,j))
				mask[i*d:(i+1)*d,j*d:(j+1)*d] = maskroi
		
		seval = np.zeros((noclus, nofeat, 2))
		for i in range(noclus):
			for j in range(nofeat):
				seval[i][j][0] = 0
				seval[i][j][1] = 255

		features = np.zeros((len(lst),nofeat))
		for ii in range(len(lst)):
			i, j = lst[ii]
			features [ii] = total_features[i*r/d +j]

		print "clustering..with pso"
		gbest, cluselem , clussize = pso.pso(nofeat,noclus,seval,features)
		print "done with clustering."

		print "data points are:"
		for i,j in enumerate(clussize):
			print "cluster",i,"contains",j,"elements"
		print "global best=",gbest

		saveimg(clussize, cluselem, "pso", it)

		print "clustering..with woa"
		gbest, cluselem , clussize = WOA.woa(nofeat,noclus,seval,features)
		print "done with clustering."

		print "data points are:"
		for i,j in enumerate(clussize):
			print "cluster",i,"contains",j,"elements"
		print "global best=",gbest

		saveimg(clussize, cluselem, "woa", it)


	return woafeatures,psofeatures

enhancedtumour = "D:\\enhanced\\"
enhancednontumour = "D:\\images\\"

#enhance.enhtumour()
#enhance.enhnontumour()

images = [image for image in os.listdir(enhancedtumour)]
woa ,pso = getclus(images)
target = [1 for i in range(len(images))]

images = [image for image in os.listdir(enhancednontumour)]
woan ,pson = getclus(images)
targetn = [0 for i in range(len(images))]

woa += woan
pso += pson
target += targetn

clf_woa = SVC(kernel = "poly", degree = 2)
clf_woa.fit(woa, target)

clf_pso = SVC(kernel = "poly", degree = 2)
clf_pso.fit(pso, target)

