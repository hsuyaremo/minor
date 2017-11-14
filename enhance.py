import matplotlib.pyplot as plt
import cv2
import numpy as np
import os
import dicom

enhanced = "D:\\enhanced\\"

def valid(x, y, rs, cs, thresh):
	if 0 <= x and x <= rs-1 and 0 <= y and y <= cs-1 and thresh[x][y] == 255:
		return 1
	else : return 0

def skstr(img):

	mf = cv2.medianBlur(img, ksize = 5)
	rows, cols = img.shape
	ti = np.mean(mf)

	l = rows
	r = 0
	u = rows
	d = 0

	for i in range(rows):
		for j in range(cols):
			if ti < mf[i][j]:
				break
		if j != cols:
			l = min(l,j)

		for j in range(rows-1,0,-1):
			if ti < mf[i][j]:
				break
		if j != rows:
			r = max(r,j)

		for j in range(rows):
			if ti < mf[j][i]:
				break
		if j != rows:
			u = min(u,j)

		for j in range(rows-1,0,-1):
			if ti < mf[j][i]:
				break
		if j != rows:
			d = max(d,j)

	roi = mf[u:d+1,l:r+1]
	tf = np.mean(roi)
	ls = [l,r,u,d]

	t,thresh = cv2.threshold(mf,tf*51.0/50.0,255,0)

	kernel = np.ones((13,13),dtype = np.uint8)
	opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

	thresh = opening
	lst = [[] for i in range(rows*cols)]

	comp = 0 
	queue = []
	col = 255
	imgvis = np.zeros((rows, cols) ,dtype = int)
	for i in range (rows):
			for j in range(cols):
				if thresh[i][j] == col and imgvis[i][j] == 0 :
					queue.append((i,j))
					imgvis[i][j] = 1
					while len(queue) != 0:
						x,y = queue.pop(0)
						lst[comp].append((x,y))
						for ii in [0,-1,1]:
							for jj in [0,-1,1]:
								if valid(x+ii,y+jj,rows,cols,thresh) and imgvis[x+ii][y+jj] == 0 :
									queue.append((x+ii,y+jj))
									imgvis[x+ii][y+jj] = 1
					comp += 1
	maxcomp = 0
	maxind = 0
	for i in range(comp):
		smlst = lst[i]
		x,y = smlst[0]
		if thresh[x][y] == 255 and maxcomp < len(smlst):
			maxcomp = len(smlst)
			maxind = i
	
	image = np.zeros((rows,cols),dtype=np.uint8)

	for i,j in lst[maxind]:
		image[i][j] = 255

	kernel = np.ones((21,21),dtype = np.uint8)
	closing = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)

	im_th = closing
	im_floodfill = im_th.copy()
	h, w = im_th.shape[:2]
	mask = np.zeros((h+2, w+2), np.uint8)
	cv2.floodFill(im_floodfill, mask, (0,0), 255);
	im_floodfill_inv = cv2.bitwise_not(im_floodfill)
 	im_out = im_th | im_floodfill_inv

 # 	dilation = cv2.dilate(im_out,kernel,iterations = 1)

 # 	l = rows
	# r = 0
	# u = rows
	# d = 0
	# ti = 0
 # 	for i in range(rows):
	# 	for j in range(cols):
	# 		if ti < im_out[i][j]:
	# 			break
	# 	if j != cols:
	# 		l = min(l,j)

	# 	for j in range(rows-1,0,-1):
	# 		if ti < im_out[i][j]:
	# 			break
	# 	if j != rows:
	# 		r = max(r,j)

	# 	for j in range(rows):
	# 		if ti < im_out[j][i]:
	# 			break
	# 	if j != rows:
	# 		u = min(u,j)

	# 	for j in range(rows-1,0,-1):
	# 		if ti < im_out[j][i]:
	# 			break
	# 	if j != rows:
	# 		d = max(d,j)
	# print l,r,u,d
 # 	winw = (r-l)/4
 # 	win = mf[d-winw:d,(l+r)/2 - winw/2 : (l+r)/2 + winw/2]
 # 	for i in range(0,d-u-winw,winw):
 # 		mf[u+i:u+winw+i,(l+r)/2 - winw/2 : (l+r)/2 + winw/2] = int(np.mean(win))
 # 	cv2.imshow('img',mf)
 # 	cv2.waitKey(0)
 # 	cv2.destroyAllWindows()
 	return im_out,mf,ls

def enhance_image(image, name, imgcnt):
	name = name[:-4]
	plt.imsave(enhanced + str(imgcnt) + ".jpg", image, cmap = "gray")
	image = cv2.imread(enhanced + str(imgcnt) + ".jpg" , 0)
	image = cv2.resize(image , (512,512))
	nonoise = cv2.fastNlMeansDenoising(image,10,10,7,21) #noise removal
	clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8)) 	#histogram equalisation
	image = clahe.apply(nonoise)
	plt.imsave(enhanced + str(imgcnt) + ".jpg", image, cmap = "gray")

def enhtumour():
	imgcnt = 0
	training_data = "D:\\trainingtumourdata\\"
	for root, dr, files in os.walk(training_data):
		for name in files:
			print "Enhancing....\n",name
			img = dicom.read_file(os.path.join(root,name))
			piarr = img.pixel_array
			enhance_image(piarr, name ,imgcnt)
			imgcnt += 1
			print "saved.",imgcnt

def enhnontumour():
	imgcnt = 0
	training_data = "D:\\trainingnontumourdata\\"
	for root, dr, files in os.walk(training_data):
		for name in files:
			print "Enhancing....\n",name
			img = dicom.read_file(os.path.join(root,name))
			piarr = img.pixel_array
			enhance_image(piarr, name ,imgcnt)
			imgcnt += 1
			print "saved.",imgcnt

#enh()




