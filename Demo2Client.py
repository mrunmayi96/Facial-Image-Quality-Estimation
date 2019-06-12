import os,sys
import json,time


hostName = "aditya"
jobId = "20180503-094000-45e6"
portNum = "5678"
folderName = "/home/aditya/Desktop/BE_Project/datafolder/digits/data"
textFile = "va2.txt"
predFile = "predictionV2.json"

imagesFolder = "ClientImages2"

scp_var = "admin1@192.168.0.13:Desktop/BE_Project/FinalDemo/Demo2"

start = time.time()
cmd = "curl localhost:"+portNum+"/models/images/classification/classify_many.json -XPOST -F job_id="+jobId+" -F image_list=@"+folderName+"/"+textFile+" > "+predFile
#print "\nPrediction Command : ",cmd	
res = os.system(cmd)
#print "\nPrediction Result : ",res

#Read json
data = []
with open(predFile) as f:
	data=json.load(f)

#Select and forward only "good" quality images
for dirName, subDirList, fileList in os.walk(folderName+"/"+imagesFolder):
	if(len(fileList) > 0):
		fileList.sort()
	
	for img in fileList:
		fname = "/data/"+imagesFolder+"/"+img
		if(data["classifications"][fname][0][0] == 'Good'):
			print ("\n"+fname+" Accepted!")
			scp_cmd = "scp " + folderName + "/" +imagesFolder + "/" +img + " " + scp_var
			#print "\nSCP Command : ",scp_cmd
			ret = os.system(scp_cmd)
			#print "\nRet : ",ret
		else:
			print ("\n"+fname+" Rejected")

end = time.time()

print ("Duration : " + str(round((end-start),3)) + "sec")




