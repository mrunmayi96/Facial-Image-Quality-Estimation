import os, os.path
import pandas as pd
import time


hostname = "admin1"	#change to your PC username before running
BEST_IMAGE1 = 0			#global variable used to store index of the best image in each folder
BEST_IMAGE2 = 0	


#-------------------------------------------------------------------------------------------------------------------------------------------------------------


def findBestImage(dirName, image_indices, chunk_count, chunk_size):
	
	
	path = dirName
	l_no = 1
	x,folderName=path.split("ToRun/")
	new_image_indices=[0]*chunk_count		#creates an empty array to store best image from each chunk in current iteration
	array_index=0							#variable used to iterate over above array while filling it with best image from each chunk
	minIndex = 0							#used to find the row in matrix of least score sums
	global BEST_IMAGE1						#at end of function this variable is assigned with the index of best image
	global BEST_IMAGE2						#at end of function this variable is assigned with the index of best image
	
	n = len(image_indices)	
	
	#iterates over current images in form of chunks
	for k in range(1, n+1, chunk_size):
		
		print "\n\nChunk: " + str(k) + " to " + str(k+9)
		w = chunk_size
		h = chunk_size
		Matrix = [[100 for x in range(w)] for y in range(h)]
		row = 0
		
		#iterates within chunk for 1st image 
		for i in range(k,k+chunk_size):
			
			if((i-1)>=len(image_indices)):
				break
			
			p = image_indices[i-1]
			img1 = dirName + "/" + folderName+"_" +str(p) + ".pgm"
			
			col = 0
			#iterates within chunk for 2nd image 
			for j in range(k, k+chunk_size):
				
				if((j-1)>=len(image_indices)):
					break
						
				q = image_indices[j-1]
				img2 = dirName + "/" + folderName+"_" +str(q) + ".pgm"
				
				if col>row:		#fill upper triangular matrix
					cmd = "python /home/"+hostname+"/openface/demos/compare.py "+img1 +" "+ img2+" 1> /home/"+hostname+"/Desktop/BE_Project/score.txt 2> /home/"+hostname+"/Desktop/BE_Project/errors.txt"
					ret = os.system(cmd)
					
					#print "img1: ",str(p)," img2: ",str(q)
					
					if ret != 0:	#handles OpenFace error cases
						Matrix[row][col] = 100.0
						Matrix[col][row] =100.0
					
					else:			#in normal case get OpenFace score from text file and write it in Matrix
						fd = open("/home/"+hostname+"/Desktop/BE_Project/score.txt", 'r')
						str_score = fd.read()
						c, score = str_score.split(": ")
						score = float(score)
						Matrix[row][col] = score
						Matrix[col][row] = score
				
				elif col == row:	#matrix diagonals are 0
					Matrix[row][col] = 0.0
			
				col = col + 1
			#outside 'j' for loop within 'i' for loop
			row = row + 1
		
		#outside 'i' for loop within 'k' for loop
				
		score_sum = list(xrange(chunk_size))			#create a list to store sum of each row of matrix
		
		for n in range(0,chunk_size):
			score_sum[n] = sum(Matrix[n])				#calculate sum of each row of matrix
		print "Match Score Sums: " + str(score_sum)
		
		minIndex = score_sum.index(min(score_sum))		#find row with least sum in matrix 
		minIndex -= 1		
		if chunk_count == 1:							#in final iteration when there is only 1 chunk 
			new_image_indices[0] = image_indices[minIndex] 
		else:
			#new_image_indices[array_index]=array[k+minIndex]										#in earlier iterations with multiple chunks
			new_image_indices[array_index]=image_indices[k+minIndex]	#store best image from chunk in array
			array_index+=1								#update array index counter variable
		
		print "In k image indices: ",new_image_indices	
	#outside 'k' for loop
	
	#calculations for next recursion
	if chunk_count > 10:			#when there are more than 10 chunks ie more than 10 best images from chunks
		if chunk_count % 10 == 0:
			new_chunk_count = chunk_count/10
			new_chunk_size = 10
		else:
			new_chunk_count = (chunk_count/10) + 1
			new_chunk_size = 10
	else:							#when there are less than 10 best images from chunks
		new_chunk_size = len(new_image_indices)
		new_chunk_count = 1
		
	
	#recursion condition is more than 1 chunk == more than 1 best image from chunks
	if (len(new_image_indices) == 1):
		BEST_IMAGE1 = new_image_indices[0]
	
	elif (len(new_image_indices) == 2):
		BEST_IMAGE1 = new_image_indices[0]
		BEST_IMAGE2 = new_image_indices[1]
	else:
		print "\nBest Images from Level "+ str(l_no) +" Chunks: "
		l_no+=1
		print new_image_indices
		findBestImage(dirName, new_image_indices, new_chunk_count, new_chunk_size)	

		
#-------------------------------------------------------------------------------------------------------------------------------------------------------------		
	
for dirName, subDirList, fileList in os.walk("/home/"+hostname+"/Desktop/BE_Project/Datasets/ChokePointSorted/ToRun"):
	if(len(fileList) > 0):
		fileList.sort()
		output  = os.popen('ls '+dirName+' -1 | wc -l').readlines() 
		num_files = int(output[0])
		
		start = time.time()
		
		print "\n\n--------------------------------------------------------------------------------"
		print "\t DIRECTORY: " + dirName
		print "\t Number of Images: ", num_files
		print "\t Starting Time : ", str(time.strftime("%a, %d %b %Y %X", time.localtime()))
		print "--------------------------------------------------------------------------------\n\n"
		
		if num_files % 10 == 0:
			chunk_count = num_files/10
			chunk_size = 10
		else:
			chunk_count = (num_files/10) + 1
			chunk_size = 10
		
		print "chunk_count: " ,chunk_count
		print "chunk_size: " ,chunk_size
		
		image_indices = list(range(1,num_files+1))
		
		findBestImage(dirName, image_indices, chunk_count, chunk_size)	#first function call
		
		print "\n\nBest image(s) from folder "+dirName+": " + str(BEST_IMAGE1) + " and " + str(BEST_IMAGE2)
		
		end = time.time()
		
		duration = end - start
		
		print "\t DIRECTORY: " + dirName + " OVER !!"
		print "\t Ending Time : ", str(time.strftime("%a, %d %b %Y %X", time.localtime()))
		print "\n\t EXECUTION TIME: ",duration
		print "--------------------------------------------------------------------------------\n\n\n"
		
		string = "\nDirectory: " + dirName + " BEST IMAGE(s) " + str(BEST_IMAGE1) + " and " + str(BEST_IMAGE2)
		
		f = open("/home/"+hostname+"/Desktop/BE_Project/ChokePoint_BestImages.txt", 'a')
		f.write(string)

