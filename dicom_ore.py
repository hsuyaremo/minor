import numpy as np
import dicom
import os
import matplotlib.pyplot as plt
import skimage
import scipy

INPUT_FOLDER = "D:\\data\\cancer\\TCGA-02-0003\\1.3.6.1.4.1.14519.5.2.1.1706.4001.145725991542758792340793681239\\1.3.6.1.4.1.14519.5.2.1.1706.4001.100169298880243060237139829068"

slices = [dicom.read_file(INPUT_FOLDER + '\\' + s) for s in os.listdir(INPUT_FOLDER)]

image = np.stack([s.pixel_array for s in slices])

image = image.astype(np.int16)

image[ image == -2000] = 0

'''
for sn in range(len(slices)):
    
    intercept = slices[sn].RescaleIntercept
    slope = slices[sn].RescaleSlope

    if slope != 1:
        image[sn] = slope * image[sn].astype(np.float64)
        image[sn] = image[sn].astype(np.int16)

    image[sn] += np.int16(intercept)
'''

hu = np.array(image ,dtype=np.int16)

'''
plt.hist(hu[20].flatten(), bins=80, color='c')
plt.xlabel("Hounsfield Units (HU)")
plt.ylabel("Frequenc
y")
plt.show()

plt.imshow( hu[20] ,cmap=plt.cm.gray)
plt.show()
'''
print slices[2]

k=3

for i in range(11):
    for j in range(11):
        b_image = np.array(hu[k] > i*10+j, dtype=np.int8)+1
        if j == 0 :
            b = b_image 
        else :
            b = np.concatenate((b,b_image),axis=1)
    if i == 0 :
        c = b
    else :
        c = np.concatenate((c,b),axis = 0)

#print c.shape
#plt.imsave('C:\\Users\\Aayush\\Desktop\\image2.png',c)
#plt.figure(figsize = (15,15))
#plt.imshow( c ,cmap="gray")
#plt.show()


