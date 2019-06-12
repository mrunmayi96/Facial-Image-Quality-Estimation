#!/usr/bin/env python2
#
# Example to compare the faces in two images.
# Brandon Amos
# 2015/09/29
#
# Copyright 2015-2016 Carnegie Mellon University
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import time

start = time.time()

import argparse
import cv2
import itertools
import os

import numpy as np
np.set_printoptions(precision=2)

import openface
import pandas as pd

df = pd.DataFrame()

start = time.time()
    

fileDir = os.path.dirname(os.path.realpath(__file__))
modelDir = os.path.join(fileDir, '..', 'models')
dlibModelDir = os.path.join(modelDir, 'dlib')
openfaceModelDir = os.path.join(modelDir, 'openface')

parser = argparse.ArgumentParser()

parser.add_argument('imgs', type=str, nargs='+', help="Input images.")
parser.add_argument('--dlibFacePredictor', type=str, help="Path to dlib's face predictor.",
                    default=os.path.join(dlibModelDir, "shape_predictor_68_face_landmarks.dat"))
parser.add_argument('--networkModel', type=str, help="Path to Torch network model.",
                    default=os.path.join(openfaceModelDir, 'nn4.small2.v1.t7'))
parser.add_argument('--imgDim', type=int,
                    help="Default image dimension.", default=96)
parser.add_argument('--verbose', action='store_true')

args = parser.parse_args()

if args.verbose:
    print("Argument parsing and loading libraries took {} seconds.".format(
        time.time() - start))

start = time.time()
align = openface.AlignDlib(args.dlibFacePredictor)
net = openface.TorchNeuralNet(args.networkModel, args.imgDim)
if args.verbose:
    print("Loading the dlib and OpenFace models took {} seconds.".format(
        time.time() - start))


def getRep(imgPath):
    if args.verbose:
        print("Processing {}.".format(imgPath))
    bgrImg = cv2.imread(imgPath)
    if bgrImg is not None:
	    rgbImg = cv2.cvtColor(bgrImg, cv2.COLOR_BGR2RGB)

	    if args.verbose:
		   print("  + Original size: {}".format(rgbImg.shape))

	    start = time.time()
	    bb = align.getLargestFaceBoundingBox(rgbImg)

	    if bb is not None:
			alignedFace = align.align(args.imgDim, rgbImg, bb,landmarkIndices=openface.AlignDlib.OUTER_EYES_AND_NOSE)
	
			if alignedFace is not None:
				rep = net.forward(alignedFace)
				     
			return rep

    else:
    	return [0 for i in range(0,128)]    
    
    
arguments = list(set(args.imgs))
arguments.sort()
#print "args: ", args.imgs
num = len(arguments)
Matrix = [0 for x in range(30)]
img1 = arguments[0]

count = 1
for img2 in arguments:
	
	if img2 != img1:
	
	    	r1 = getRep(img1)
	    	r2 = getRep(img2)
	    	if (all(i == 0 for i in r1) or all(j == 0 for j in r2)):
				d = 3
	    	else:
				d = r1 - r2
	    	#print("Comparing {} with {}.".format(img1, img2))
	    	score = round(np.dot(d,d), 3)
	    	#temp = "{\"S" + str(count) + "\":" + str(round(score,3)) + "}"
	    	#print("S"+str(count)+": {:0.3f}".format(np.dot(d, d)))
	    	#print temp
	    	Matrix[count] = score
	    	print score
	    	count += 1
	    	

    	
	
