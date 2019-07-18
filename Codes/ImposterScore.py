#!/usr/bin/python

import os, os.path
import pandas as pd
import time
#import sys

#sys.path.append('/usr/local/lib/python2.7/site-packages')

#For Alisha
#Find and replace all 'aditya' with 'admin1'
#Also check the directory name of 'ChokePointSorted

df = pd.DataFrame()

'''
for actual implementation:
range of i: 1 to 150
range of j: 1 to 31
range of k: 1 to 31
'''
start_time = time.time()
print "\nStart time is: "+str(time.strftime("%a, %d %b %Y %X", time.localtime()))+"\n\n"
for i in range(1, 56):
	for j in range(1, 31):
		if(j!=8):
			temp = j + 1			
			for k in range(temp, 31):
				if(k != 8):
					#print i, j, k
					#print "\n"
			
					temp_i =str(i);
				
					if(j<10):
						temp_j ="0"+str(j);
					else:
						temp_j =str(j);
				
					if(k<10):
						temp_k ="0"+str(k);
					else:
						temp_k =str(k);
			
					file1="/home/admin1/Desktop/BE_Project/Datasets/ChokePointSorted/S"+temp_j+"/S"+temp_j+"_"+temp_i+".pgm"
					file2="/home/admin1/Desktop/BE_Project/Datasets/ChokePointSorted/S"+temp_k+"/S"+temp_k+"_"+temp_i+".pgm"
					cmd = "python /home/admin1/openface/demos/compare.py "+file1+" "+file2+" 1> /home/admin1/Desktop/BE_Project/score.txt 2> /home/admin1/Desktop/BE_Project/errors.txt"
					ret = os.system(cmd)
			
					img1="S"+temp_j+"_"+temp_i+".pgm"
					img2="S"+temp_k+"_"+temp_i+".pgm"
			
					#print file1, file2
			
					#print img1, img2
			
					if ret != 0:
						d=[img1, img2, 100]
						data=[d]
						df_temp = pd.DataFrame(data, columns=['Face1','Face2','MatchScore'], dtype = float)
						df = df.append(df_temp)
						df.to_csv('/home/admin1/Desktop/BE_Project/Imposter_Scores.csv')
						print img1 +" "+ img2 + " compared unsuccessfully"
	
					else:	
						fd = open("/home/admin1/Desktop/BE_Project/score.txt", 'r')
						str_score = fd.read()
						c, score = str_score.split(": ")
						score = float(score)
						d=[img1, img2, score]
						data=[d]
						df_temp = pd.DataFrame(data, columns=['Face1','Face2','MatchScore'], dtype = float)
						df = df.append(df_temp)
						df.to_csv('/home/admin1/Desktop/BE_Project/Imposter_Scores.csv')
						print img1 +" "+ img2 + " compared successfully"

end_time = time.time()
total_time = end_time - start_time
print "\n\nThe total execution time is: "+str(total_time)
print "\nEnd time is: "+str(time.strftime("%a, %d %b %Y %X", time.localtime()))+"\n\n"
print "\nExiting program now...\n"


