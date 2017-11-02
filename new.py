import numpy as np 
import dicom
import os
import scipy.ndimage
import matplotlib.pyplot as plt
from skimage import exposure
from skimage import data, img_as_float
from skimage import measure, morphology
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

INPUT_FOLDER = "D:\\data\\cancer\\TCGA-02-0003\\1.3.6.1.4.1.14519.5.2.1.1706.4001.145725991542758792340793681239\\"

patients = os.listdir(INPUT_FOLDER)
patients.sort()



def load_scan(path):
    slices = [dicom.read_file(path + '\\' + s) for s in os.listdir(path)]
    slices.sort(key = lambda x: float(x.ImagePositionPatient[2]))
    try:
        slice_thickness = np.abs(slices[0].ImagePositionPatient[2] - slices[1].ImagePositionPatient[2])
    except:
        slice_thickness = np.abs(slices[0].SliceLocation - slices[1].SliceLocation)
        
    for s in slices:
        s.SliceThickness = slice_thickness
        
    return slices



def get_pixels(slices):
    image = np.stack([s.pixel_array for s in slices])
    image = image.astype(np.int16)

    image[image == -2000] = 0
    return np.array(image, dtype=np.int16)
    

first_patient = load_scan(INPUT_FOLDER + patients[0])
first_patient_pixels = get_pixels(first_patient)

c_image = first_patient_pixels[10]

plt.hist(c_image.flatten(), color='c')
plt.xlabel("pixel values")
plt.ylabel("Frequency")
plt.show()

combine = c_image;

plt.imshow(np.float64(c_image), cmap=plt.cm.gray)
plt.show()

img_eq = exposure.equalize_adapthist(c_image)
b_image = np.array(c_image > 50, dtype=np.int8)+1

print img_eq.dtype
plt.imshow(img_eq, cmap = "gray")
plt.show()
plt.hist(img_eq.flatten(),color='r')
plt.show
plt.imshow(b_image,cmap = "gray") 
plt.show()
b_after_hist_equil = np.array(img_eq > 0.0010000, dtype=np.int8)+1
plt.imshow(b_after_hist_equil,cmap = "gray") 
plt.show()

