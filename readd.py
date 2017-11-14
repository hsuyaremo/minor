import matplotlib.pyplot as plt
import dicom
import numpy as np
import cv2
import os
import pso
import WOA
import feature
import enhance


training_data = "D:\\trainingdata\\"
enhanced = "D:\\enhanced\\"
testing = "D:\\images\\"
images = [name for name in os.listdir(training_data)]
noclus = 4
nofeat = 1
patchsz = 2 #patch size  
'''
print "Enhancing....\n"
for it,name in enumerate(images):
	img = dicom.read_file(training_data + name)
	piarr = img.pixel_array
	enhance.enhance_image(piarr, name)
	name = name[:-4]

print "saved."
'''
images = [name for name in os.listdir(enhanced)]

for it,name in enumerate(images):
	piarr = cv2.imread(enhanced + name ,0)
	mask ,piarr = enhance.skstr(piarr)
	'''
	cv2.imshow('mask',mask)
	cv2.waitKey(0)
	cv2.destroyAllWindows()
	
	r= piarr.shape[0]

	print "Processing image",name,"..."
	total_features = feature.feature_extraction(piarr,patchsz,nofeat)
	print "processing done."
	
	d = patchsz
	lst = []
	for i in range(r/d):
		for j in range(r/d):
			maskroi = mask[i*d:(i+1)*d,j*d:(j+1)*d]
			flag = 0
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
		
		#seval[i][2][1] = seval[i][3][1] = 16*255
		#seval[i][3][0] = seval[i][2][0] = 0

	print total_features.shape
	
	features = np.zeros((len(lst),nofeat))
	for ii in range(len(lst)):
		i, j = lst[ii]
		features [ii] = total_features[i*r/d +j]
	print "clustering.."
	gbest, cluselem , clussize = WOA.woa(nofeat,noclus,seval,features)
	print "done with clustering."

	print "data points are:"
	for i,j in enumerate(clussize):
		print "cluster",i,"contains",j,"elements"
	print "global best=",gbest

	brainarea = len(lst)
	smallest_clus_size = len(lst)+1
	smallest_clus_index =-1
	for i,j in enumerate(clussize):
		if smallest_clus_size > j and j > brainarea/20:
			smallest_clus_size = j
			smallest_clus_index = i 
	
	noclus = 2
	feat = np.array([features[cluselem[smallest_clus_index][i]] for i in range(smallest_clus_size)])
	gbe, tumelem , tumsize = WOA.woa(nofeat,noclus,seval,feat)


	print "data points are:"
	for i,j in enumerate(tumsize):
		print "cluster",i,"contains",j,"elements"
	print "global best=",gbe

	seg_imag = np.zeros((r,r),dtype = np.uint8)
	seg_tumor = np.zeros((r,r),dtype = np.uint8)
	col = [50,125,200,255]

	for i in range(tumsize.shape[0]):
		for j in range(tumsize[i]):
			ii, jj = lst[cluselem[smallest_clus_index][tumelem[i][j]]]
			seg_imag[ii*patchsz:(ii+1)*patchsz,jj*patchsz:(jj+1)*patchsz] = col[i]
	
	for j in range(clussize[smallest_clus_index]):
		ii, jj = lst[cluselem[smallest_clus_index][j]]
		seg_tumor[ii*patchsz:(ii+1)*patchsz,jj*patchsz:(jj+1)*patchsz] = col[i]
	
	cv2.imshow('img',seg_imag)
	cv2.imshow('tumor',seg_tumor)
	noclus = 4
	cv2.waitKey(0)
	cv2.destroyAllWindows()
	plt.imsave(testing+"woa_clus4"+str(it)+".jpg",seg_imag);
	'''
	


	
