# -*- conding: utf-8 -*-
import os
import sys

from scipy import misc
import numpy as np
import matplotlib.pyplot as plt
import math

# import mydip

import pdb

def mypredict(P):
	T = (P[2][0]-P[1][0])*(P[2][1]-P[3][1])-(P[2][0]-P[3][0])*(P[2][1]-P[1][1]);

	G_=((P[2][0]-P[0][0])*(P[2][1]-P[3][1])-(P[2][0]-P[3][0])*(P[2][1]-P[0][1]))/T;
	H_=((P[2][0]-P[1][0])*(P[2][1]-P[0][1])-(P[2][0]-P[0][0])*(P[2][1]-P[1][1]))/T;

	A=G_*(P[1][0]-P[0][0]);
	D=G_*(P[1][1]-P[0][1]);
	B=H_*(P[3][0]-P[0][0]);
	E=H_*(P[3][1]-P[0][1]);

	G=G_-1;
	H=H_-1;
	C=0;
	F=0;
	I=1;
	return ((A,B,C),(D,E,F),(G,H,I));

def mykeystone(img, P, interp, boundary, kernel, k):
	
	h, w, c = img.shape
	out = np.zeros(h*w*c).reshape(h,w,c)
	
	M_ = mypredict(P);
	M_ = np.dot(M_, np.diag((1.0/w, 1.0/h, 1.0)))
	M = np.linalg.inv(M_)	

	for y in range(0,h):
		for x in range(0,w):	
			# print y, x
			T =   M[2][0]*x + M[2][1]*y + M[2][2];
			nx = (M[0][0]*x + M[0][1]*y + M[0][2])/T + 0;
			ny = (M[1][0]*x + M[1][1]*y + M[1][2])/T + 0;

			if nx < 0 or nx > w-1 or ny < 0 or ny > h-1:
				out[y,x,:] = 0
				continue;
			#print x, y, nx, ny
			dx = nx - np.floor(nx)
			dy = ny - np.floor(ny)
			
			fx = min(max(np.floor(nx),0), w-1)
			fy = min(max(np.floor(ny),0), h-1)
			cx = min(max(np.ceil(nx),0), w-1)
			cy = min(max(np.ceil(ny),0), h-1)
		
			# boundary condition
			# print fx, fy, cx, cy, dx, dy
			new_pixel = img[fy,fx,:]*(1-dx)*(1-dy) + \
						img[cy,fx,:]*(1-dx)*(  dy) + \
						img[fy,cx,:]*(  dx)*(1-dy) + \
						img[cy,cx,:]*(  dx)*(  dy)
			out[y,x,:] = new_pixel
			
	return out


if __name__ == "__main__" :
	#pdb.set_trace()
		# mydip.imshow(img, 0)
		img = misc.imread('keystone2.jpg')
		P = ((0.0, 0.0), (np.size(img,1), 0.0), (np.size(img,1)-180 , np.size(img,0)), (180.0, np.size(img,0)))
		out = mykeystone(img, P, 'default', 'default', 'default', 'default')
		misc.imsave('output.bmp',  out)


