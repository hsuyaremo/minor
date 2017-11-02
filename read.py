from matplotlib import pyplot
import dicom
import cv2
import numpy 

D = dicom.read_file("D:\\data\\cancer\\TCGA-02-0003\\1.3.6.1.4.1.14519.5.2.1.1706.4001.145725991542758792340793681239\\1.3.6.1.4.1.14519.5.2.1.1706.4001.273700949846991110226831783061\\000058.dcm")

array = numpy.zeros((D.Rows,D.Columns), dtype=D.pixel_array.dtype)
array = D.pixel_array

x = numpy.arange(0.0, 256*D.PixelSpacing[0], D.PixelSpacing[0])
y = numpy.arange(0.0, 256*D.PixelSpacing[1], D.PixelSpacing[1])

"""
pyplot.figure(dpi=300)
pyplot.axes().set_aspect('equal', 'datalim')
pyplot.set_cmap(pyplot.gray())
pyplot.pcolormesh(x, y, numpy.flipud(array[:, :]))
"""
fil = open("array.txt","w")
print D.pixel_array.dtype

#cv2.imshow('image' ,D.pixel_array )



I = cv2.imread('prism.png',cv2.IMREAD_GRAYSCALE)
I8 = numpy.uint8((array+1)/2 *255)

print D

cv2.imshow('image',I8)


cv2.waitKey(0)
cv2.destroyAllWindows()

