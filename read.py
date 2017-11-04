import matplotlib.pyplot as plt
import dicom
import os
import pso
import WOA
import numpy as np

training_data = "D:\\trainingdata\\"
images = [name for name in os.listdir(training_data)]
noclus = 5
nofeat = 1
	
def feature_extraction(image):
	d = 4
	dpoint = np.zeros((512/d*512/d,nofeat))
	for i in range(512/d):
		for j in range(512/d):
			roi = image[i*d:(i+1)*d,j*d:(j+1)*d]
			mean = 0.0
			for x in roi.flatten():
				mean +=x
			mean /= (d*d*1.0)
			dpoint[i*512/d + j][0] = mean

	return dpoint

for name in images:
	d = dicom.read_file(training_data + name)
	piarr = d.pixel_array
	print "processing image",name,"..."
	features = feature_extraction(piarr)
	print "processing done."
	seval = np.zeros((noclus, nofeat, 2))
	for i in range(noclus):
		for j in range(nofeat):
			seval[i][j][0] = 0
			seval[i][j][1] = 260
	
	print max(features.flatten())
	print "clustering.."
	gbest, cluselem , clussize = pso.pso(nofeat,noclus,seval,features)
	print "done with clustering."

	print "data points are:"
	for i,j in enumerate(clussize):
		print "cluster",i,"contains",j,"elements"
	print "global best=",gbest

	seg_imag = piarr

	for i in range(noclus):
		for j in range(clussize[i]):
			dpoint = cluselem[i][j]
			ii = dpoint/128
			jj = dpoint%128
			seg_imag[ii*4:(ii+1)*4,jj*4:(jj+1)*4] = i*10
	plt.imshow(seg_imag)
	plt.show()

	