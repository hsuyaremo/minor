from matplotlib import pyplot
import dicom
import os
import pso
import WOA
import numpy as np 

training_data = "D:\\trainingdata\\"
images = [name for name in os.listdir(training_data)]

def feature_extraction(image):
	fdtype = "float64"
	dpoint = np.zeroes((128*128), dtype = fdtype)
	for i in range(128):
		for j in range(128):
			roi = image[i*4:(i+1)*4 - 1][i*4:(i+1)*4 - 1]
			mean = 0
			for x in roi.flatten():
				mean +=x;
			mean /= 16;
			dpoint[i*128 + j][0] = mean;
	return dpoint

for name in images:
	d = dicom.read_file(training_data + name)
	piarr = d.pixel_array
	features = feature_extraction(piarr)
	noclus = 5
	nofeat = 1
	seval = np.zeroes((noclus,2), dtype = "float64")
	feat_set = ["float64"]
	seval[0][0] = 100 
	seval[0][1] = 150
	gbest, cluselem = pso.pso(feat_set,nofeat,noclus,seval)